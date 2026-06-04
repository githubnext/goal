# Install Goal

This prompt guides you, a coding agent, to install **Goal** in a repository.
Goal is an agentic workflow that works labeled GitHub issues until their
completion contract is satisfied by evidence.

## Your Task

Set up Goal in this repository by:

1. Installing the `gh-aw` CLI extension.
2. Initializing the repository for GitHub Agentic Workflows.
3. Copying Goal workflow files and the Goal issue form.
4. Compiling the workflow.
5. Creating the `goal` and `goal-completed` labels.
6. Adding agent instructions so generated workflow files stay fresh.
7. Creating a branch, committing, and opening a pull request.
8. Helping the user create their first strong goal issue.

## Step 1: Install gh-aw CLI Extension

Install the extension directly through GitHub CLI:

```bash
gh extension install github/gh-aw
```

Verify installation:

```bash
gh aw version
```

If this fails, check that `gh` is installed and authenticated:

```bash
gh --version
gh auth status
```

## Step 2: Initialize Agentic Workflows

```bash
gh aw init
```

This configures the repository for Agentic Workflows.

## Step 3: Download Goal And Copy Files

Download the Goal source as a zip and copy the workflow files and issue form
into this repository.

### Linux And macOS

```bash
curl -fL https://github.com/githubnext/goal/archive/refs/heads/main.zip -o /tmp/goal.zip
unzip -q /tmp/goal.zip -d /tmp/goal_extract

mkdir -p .github/workflows .github/ISSUE_TEMPLATE

cp -R /tmp/goal_extract/goal-main/workflows/. .github/workflows/
cp -R /tmp/goal_extract/goal-main/.github/ISSUE_TEMPLATE/. .github/ISSUE_TEMPLATE/

rm -rf /tmp/goal.zip /tmp/goal_extract
```

If `unzip` is not available, replace the unzip line with:

```bash
mkdir -p /tmp/goal_extract && tar -xf /tmp/goal.zip -C /tmp/goal_extract
```

### Windows PowerShell

```powershell
Invoke-WebRequest -Uri "https://github.com/githubnext/goal/archive/refs/heads/main.zip" -OutFile "$env:TEMP\goal.zip"
Expand-Archive -Path "$env:TEMP\goal.zip" -DestinationPath "$env:TEMP\goal_extract" -Force

New-Item -ItemType Directory -Force -Path ".github/workflows", ".github/ISSUE_TEMPLATE" | Out-Null

Copy-Item -Path "$env:TEMP\goal_extract\goal-main\workflows\*" -Destination ".github/workflows/" -Recurse -Force
Copy-Item -Path "$env:TEMP\goal_extract\goal-main\.github\ISSUE_TEMPLATE\*" -Destination ".github\ISSUE_TEMPLATE\" -Recurse -Force

Remove-Item -Path "$env:TEMP\goal.zip", "$env:TEMP\goal_extract" -Recurse -Force
```

To pin a version, replace `refs/heads/main` with `refs/tags/<tag>` and replace
`goal-main` with `goal-<tag>`.

This installs the guided Goal issue form at `.github/ISSUE_TEMPLATE/goal.yml`.
Use it when a goal is ready for the workflow to start. If the goal needs a
helper script, fixture, package script, CI target, or other setup before
doneness can be judged, create that setup PR first.

## Step 4: Compile The Workflow

```bash
gh aw compile goal
```

This generates `.github/workflows/goal.lock.yml` from
`.github/workflows/goal.md`.

## Step 5: Create Labels

Create the labels used by the workflow. If a label already exists, leave it in
place.

```bash
gh label create goal --color 0969da --description "Agentic goal workflow should continue working this issue" || true
gh label create goal-completed --color 1a7f37 --description "Agentic goal workflow completed this issue" || true
```

## Step 6: Add Agent Instructions

Add or update `AGENTS.md` with:

````markdown
## Agentic Workflows

After modifying any `.md` workflow file under `.github/workflows/`, always
recompile and commit the generated workflow files with the source change:

```bash
gh aw compile
apm compile
```

For Goal issues, keep the completion contract evidence-based. A goal is complete
only when the issue's stated verification evidence supports it.
````

If the repository uses `CLAUDE.md`, `COPILOT.md`, or another agent instruction
file, add the same note there too.

## Step 7: Commit And Open A Pull Request

```bash
git checkout -b install-goal
git add .
git commit -m "Install Goal workflow"
git push -u origin install-goal
gh pr create --title "Install Goal workflow" --body "Set up the Goal agentic workflow and issue form."
```

Report the pull request link to the user.

## Step 8: Create The First Goal With The User

Before opening or labeling a goal issue, work with the user to make the goal
very actionable. Do not settle for "fix this", "improve this", or "make it
better" if the issue does not define how completion will be proven.

Use this shaping protocol:

1. Restate the desired outcome in one sentence.
2. Ask only for missing details that cannot be discovered from the repository.
3. Turn the answer into a goal issue using the installed Goal issue form, with
   these sections:
   - `Goal`
   - `Completion Contract`
   - `Evidence / Verification`
   - `Scope and Constraints`
   - `Context To Read First`
   - `Iteration Policy`
   - `Blocked Stop Condition`
4. Decide whether an inline doneness script in the issue is enough, or whether a
   small setup PR is needed first.
5. Review the draft with the user before adding the `goal` label.
6. Once the user agrees and the goal is ready to run, create the issue and apply
   the `goal` label. If using the installed issue form, submit it only when the
   `goal` label can be applied immediately.

The distilled pattern is:

```text
Complete <desired end state>, verified by <specific evidence>, while preserving
<constraints>. Use <allowed files, tools, data, and boundaries>. Between runs,
choose the next smallest checkpoint based on the latest evidence and human
comments. If blocked or no defensible path remains, stop substantive work and
report <what failed, what is known, and what would unlock progress>.
```

A strong issue tells the workflow what "done", "not done yet", and "blocked"
mean. It should include at least one concrete verification surface: a test
command, build command, benchmark, screenshot requirement, artifact review,
log check, inline doneness script, or source-of-truth document.

### Example Strong Goal

````markdown
## Goal

Migrate the authentication tests from the legacy helper to `createTestSession`.

## Completion Contract

Every authentication test uses `createTestSession`, the legacy helper has no
remaining call sites in `tests/auth`, and the auth test suite and lint pass.

## Evidence / Verification

```bash
rg "legacyAuthHelper" tests/auth
npm test -- tests/auth
npm run lint
```

Completion requires `rg` to find no call sites and both commands to exit 0.

## Scope and Constraints

Allowed files:
- `tests/auth/**`
- `test/helpers/auth.ts`

Do not change production authentication behavior.

## Iteration Policy

Migrate one coherent test group at a time. After each run, execute the smallest
relevant test command before broadening to the whole auth suite.

## Blocked Stop Condition

If the tests need unavailable secrets or services, stop and comment with the
exact missing dependency, the command output, and the smallest next action for a
maintainer.
````

## Troubleshooting

### `gh aw compile goal` fails

- Confirm `.github/workflows/goal.md` exists.
- Confirm `.github/workflows/scripts/goal_scheduler.py` exists.
- Run `gh aw compile goal --verbose`.

### No goal issues are picked up

- Confirm the issue is open.
- Confirm the issue has the exact `goal` label.
- Confirm it has not already been relabeled `goal-completed`.
- Check the workflow run log for `/tmp/gh-aw/goal.json`.

## Reference

- Goal repository: https://github.com/githubnext/goal
- GitHub Agentic Workflows: https://github.github.com/gh-aw/
