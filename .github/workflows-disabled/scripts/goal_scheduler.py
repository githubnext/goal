#!/usr/bin/env python3
"""Goal scheduler.

Finds open GitHub issues labeled ``goal``, chooses one issue for this workflow
run, and writes ``/tmp/gh-aw/goal.json`` for the agent step.

The scheduler is intentionally small and deterministic:

* Issue title + number produce the stable branch name ``goal/<number>-<slug>``.
* The oldest ``Last Run`` in repo-memory runs first; never-run issues run first.
* The scheduler reports whether the issue definition has the required sections
  for a strong, evidence-based goal.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

GOAL_LABEL = "goal"
COMPLETED_LABEL = "goal-completed"
REPO_MEMORY_DIR = "/tmp/gh-aw/repo-memory/goal"
OUTPUT_DIR = "/tmp/gh-aw"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "goal.json")

REQUIRED_SECTIONS = {
    "goal": ("goal",),
    "completion_contract": ("completion contract", "definition of done"),
    "evidence": ("evidence / verification", "verification", "evidence"),
    "scope": ("scope and constraints", "scope", "constraints"),
    "iteration_policy": ("iteration policy", "iteration plan"),
    "blocked_stop_condition": ("blocked stop condition", "blocked condition", "blockers"),
}

PLACEHOLDER_RE = re.compile(
    r"\b(REPLACE|TODO|TBD|FIXME|YOUR_|WITH_|PLACEHOLDER)\b|\.\.\.",
    re.IGNORECASE,
)


def slugify_issue_title(title: str, number: int | None = None) -> str:
    """Return a stable branch-safe slug for a GitHub issue title."""

    slug = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    if not slug:
        slug = "issue-{}".format(number) if number is not None else "issue"
    return slug[:80].strip("-") or "issue"


def branch_for_issue(number: int, title: str) -> str:
    return "goal/{}-{}".format(number, slugify_issue_title(title, number))


def state_file_for_issue(number: int, title: str) -> str:
    return "{}-{}.md".format(number, slugify_issue_title(title, number))


def parse_link_header(header: str | None) -> str | None:
    if not header:
        return None
    for part in header.split(","):
        section = part.strip()
        match = re.match(r'^<([^>]+)>;\s*rel="next"$', section)
        if match:
            return match.group(1)
    return None


def _http_get_json(url: str, headers: dict[str, str], timeout: int = 30):
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode())
            link_header = response.headers.get("link") or response.headers.get("Link")
            return body, link_header
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, OSError):
        return None, None


def extract_markdown_sections(markdown: str) -> dict[str, str]:
    """Extract h2/h3 sections from markdown, keyed by normalized heading."""

    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in (markdown or "").splitlines():
        match = re.match(r"^\s{0,3}#{2,3}\s+(.+?)\s*$", line)
        if match:
            heading = normalize_heading(match.group(1))
            current = heading
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def normalize_heading(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text or "")
    text = re.sub(r"[^a-z0-9 /-]+", "", text.lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def has_real_content(text: str) -> bool:
    stripped = re.sub(r"<!--.*?-->", "", text or "", flags=re.DOTALL).strip()
    stripped = re.sub(r"```.*?```", "", stripped, flags=re.DOTALL).strip()
    if len(stripped) < 12:
        return False
    if PLACEHOLDER_RE.search(stripped):
        return False
    return True


def analyze_goal_definition(markdown: str) -> dict[str, object]:
    """Return readiness and missing section info for a goal issue body."""

    sections = extract_markdown_sections(markdown)
    missing: list[str] = []
    present: list[str] = []

    for field, aliases in REQUIRED_SECTIONS.items():
        matched_key = None
        for alias in aliases:
            normalized_alias = normalize_heading(alias)
            if normalized_alias in sections:
                matched_key = normalized_alias
                break
        if matched_key and has_real_content(sections.get(matched_key, "")):
            present.append(field)
        else:
            missing.append(field)

    return {
        "definition_status": "ready" if not missing else "needs_action",
        "missing_sections": missing,
        "present_sections": present,
    }


def parse_machine_state(content: str) -> dict[str, object]:
    state: dict[str, object] = {}
    match = re.search(r"## Machine State\s*\n(.*?)(?=\n## |\Z)", content or "", re.DOTALL)
    if not match:
        return state
    for row in re.finditer(r"\|\s*(.+?)\s*\|\s*(.*?)\s*\|", match.group(1)):
        key = row.group(1).strip().lower().replace(" ", "_")
        value = row.group(2).strip()
        if key in ("field", "---", ""):
            continue
        if value in ("-", "--", ""):
            value = None
        state[key] = value
    for bool_field in ("completed", "blocked"):
        if bool_field in state:
            state[bool_field] = str(state[bool_field]).lower() == "true"
    if "run_count" in state:
        try:
            state["run_count"] = int(str(state["run_count"]))
        except (TypeError, ValueError):
            state["run_count"] = 0
    return state


def read_goal_state(number: int, title: str, repo_memory_dir: str = REPO_MEMORY_DIR):
    path = os.path.join(repo_memory_dir, state_file_for_issue(number, title))
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return parse_machine_state(handle.read())


def fetch_goal_issues(repo: str, github_token: str, http_get_json=_http_get_json):
    """Fetch open issues with the goal label."""

    if not repo or not github_token:
        return []

    headers = {
        "Authorization": "token {}".format(github_token),
        "Accept": "application/vnd.github.v3+json",
    }
    label = urllib.parse.quote(GOAL_LABEL)
    next_url = (
        "https://api.github.com/repos/{}/issues"
        "?labels={}&state=open&per_page=100".format(repo, label)
    )
    issues = []
    while next_url:
        body, link_header = http_get_json(next_url, headers)
        if not isinstance(body, list):
            break
        for issue in body:
            if not isinstance(issue, dict) or issue.get("pull_request"):
                continue
            labels = [label_obj.get("name") for label_obj in issue.get("labels", [])]
            if COMPLETED_LABEL in labels:
                continue
            issues.append(issue)
        next_url = parse_link_header(link_header)
    return issues


def find_existing_pr_for_branch(repo: str, branch: str, github_token: str, http_get_json=_http_get_json):
    """Return the open PR number for a branch, if one exists."""

    if not repo or not branch or not github_token:
        return None
    owner = repo.split("/", 1)[0]
    headers = {
        "Authorization": "token {}".format(github_token),
        "Accept": "application/vnd.github.v3+json",
    }
    head = urllib.parse.quote("{}:{}".format(owner, branch), safe="")
    url = "https://api.github.com/repos/{}/pulls?head={}&state=open".format(repo, head)
    body, _ = http_get_json(url, headers)
    if isinstance(body, list) and body:
        number = body[0].get("number")
        if number:
            return number
    return None


def issue_to_goal(issue: dict[str, object], repo: str = "", github_token: str = "") -> dict[str, object]:
    number = int(issue["number"])
    title = str(issue.get("title") or "Goal")
    body = str(issue.get("body") or "")
    branch = branch_for_issue(number, title)
    analysis = analyze_goal_definition(body)
    state = read_goal_state(number, title)
    existing_pr = find_existing_pr_for_branch(repo, branch, github_token)

    return {
        "number": number,
        "title": title,
        "slug": slugify_issue_title(title, number),
        "url": issue.get("html_url"),
        "api_url": issue.get("url"),
        "updated_at": issue.get("updated_at"),
        "branch": branch,
        "state_file": state_file_for_issue(number, title),
        "last_run": state.get("last_run"),
        "run_count": state.get("run_count", 0),
        "completed": bool(state.get("completed", False)),
        "blocked": bool(state.get("blocked", False)),
        "existing_pr": existing_pr,
        **analysis,
    }


def select_goal(goals: list[dict[str, object]], forced_issue: str | None = None):
    if forced_issue:
        forced_issue = forced_issue.strip().lstrip("#")
        for goal in goals:
            if str(goal["number"]) == forced_issue:
                return goal, [g for g in goals if g is not goal], None
        return None, goals, "requested goal issue #{} was not found".format(forced_issue)

    if not goals:
        return None, [], None

    runnable = [goal for goal in goals if not goal.get("completed")]
    if not runnable:
        return None, [], None

    selected = sorted(runnable, key=lambda goal: str(goal.get("last_run") or ""))[0]
    deferred = [goal for goal in runnable if goal is not selected]
    return selected, deferred, None


def main() -> int:
    github_token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    forced_issue = os.environ.get("GOAL_ISSUE", "").strip()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    issues = fetch_goal_issues(repo, github_token)
    goals = [issue_to_goal(issue, repo, github_token) for issue in issues]
    selected, deferred, error = select_goal(goals, forced_issue)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "no_goals": not goals,
        "selected": selected,
        "deferred": deferred,
        "error": error,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, sort_keys=True)

    if error:
        print(error)
        return 1
    if selected:
        print("Selected goal #{}: {}".format(selected["number"], selected["title"]))
    else:
        print("No goal issues found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
