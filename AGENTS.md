# Goal

Goal is an agentic workflow for durable, evidence-based GitHub issue work. It is
built on GitHub Agentic Workflows and keeps one long-running branch and draft PR
per goal issue.

## Architecture

```text
goal/
|-- AGENTS.md
|-- README.md
|-- install.md
|-- workflows/
|   |-- goal.md
|   |-- shared/
|   |   `-- reporting.md
|   `-- scripts/
|       `-- goal_scheduler.py
|-- .github/
|   `-- ISSUE_TEMPLATE/
|       `-- goal.md
`-- tests/
    `-- test_goal_scheduler.py
```

## Conventions

- The workflow source is `workflows/goal.md`.
- Installed repositories copy workflow files into `.github/workflows/`.
- The scheduler writes `/tmp/gh-aw/goal.json` for the agent step.
- Active goal issues are open GitHub issues with the `goal` label.
- Completed issues have `goal-completed` and no `goal` label.
- Each issue uses the exact branch from scheduler output:
  `goal/<issue-number>-<slugified-title>`.
- The branch name must not include run IDs, suffixes, hashes, or random tokens.
- Each issue has one draft PR with title `[Goal #<issue>] <title>`.
- Every workflow run posts a new comment on the issue and updates the status
  comment marked `<!-- GOAL:STATUS -->`.
- Durable state lives in repo-memory on the `memory/goal` branch.

## Editing

After modifying any workflow markdown under `workflows/`, run tests. In an
installed target repository, also run:

```bash
gh aw compile
apm compile
```

Commit generated workflow files together with source workflow changes when they
exist.

Run the local scheduler tests with:

```bash
python3 -m unittest discover -s tests -q
```
