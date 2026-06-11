# Create A New Goal

This prompt guides you, a coding agent, to help a user create a strong Goal
workflow issue. Do not simply open an issue and add the `goal` label. First make
the goal actionable, verifiable, scoped, and safe for an agentic workflow to run
without the user steering every turn.

Goal is inspired by `/goal` in Codex and Claude Code: one durable objective, a
clear stopping condition, evidence that proves progress, and constraints that
matter. In this repository workflow, that contract lives in a GitHub issue and
the `goal` label starts the long-running Goal Agentic Workflow.

## Your Task

Work with the user to create one good goal. By the end, either:

1. Create a GitHub issue with the `goal` label.
2. Create a small setup PR and an unlabelled draft goal issue, if the repo needs
   a helper script, fixture, test harness, or other setup before the Goal
   workflow can judge doneness reliably.
3. Stop and explain what information is missing, if the goal cannot yet be made
   actionable.

Prefer keeping everything in the issue. Create a setup PR only when the issue
alone would make the Goal workflow guess or repeatedly fail.

## What Makes A Good Goal

A good goal is bigger than one prompt but smaller than an open-ended backlog. It
has:

- One objective, not a loose list of unrelated tasks.
- A verifiable stopping condition.
- A stated check: command, script, artifact, screenshot, log, file count, empty
  queue, or other evidence.
- Constraints that must hold while the work is done.
- Pointers to the files, docs, issues, logs, designs, or examples the agent must
  read first.
- Checkpoints small enough for the workflow to make progress and report clearly.
- A blocked stop condition so the workflow knows when to pause instead of
  inventing missing requirements.

Avoid vague goals such as "improve auth", "clean up tests", or "make the UI
better" unless you turn them into a concrete contract.

## Creation Flow

1. Read the repository enough to understand the user's request.
2. Restate the intended outcome in one sentence.
3. Identify what would prove the outcome is done.
4. Identify what must not change.
5. Decide whether doneness can be judged from commands or scripts written in the
   issue.
6. If not, propose the smallest setup PR that would make doneness checkable.
7. Draft the goal issue.
8. Ask the user to confirm any uncertain product, design, or policy detail.
9. Create the issue only after the contract is strong. If the Goal issue form is
   installed, use its fields so the issue body follows the same contract.
10. Add the `goal` label only when the workflow can safely start. If using the
    installed issue form, submit it only when the label can be applied
    immediately.

## Doneness Checks

The issue may include a doneness script directly in a fenced code block. This is
often the best path because the Goal workflow can copy or run the script without
requiring repo changes.

Use an inline script when:

- It only calls existing repo commands.
- It checks existing files, logs, endpoints, snapshots, or artifacts.
- It can be pasted into a shell safely.
- It does not require secrets the workflow lacks.

Example:

````markdown
## Evidence / Verification

Run this from the repository root:

```bash
set -euo pipefail
npm test -- tests/auth
npm run lint
! rg "legacyAuthHelper" tests/auth
```

Completion requires all commands to exit 0.
````

Create a setup PR when:

- The check needs a reusable helper script or fixture.
- The repo has no command that can judge the goal.
- CI needs a new target, package script, or test harness.
- The check would be too long or fragile to live only in the issue.
- The workflow needs files that should be reviewed before autonomous work
  starts.

If you create a setup PR, keep it tiny and mechanical. It should add the minimum
doneness check, not implement the goal itself. Leave the goal issue unlabelled
until that PR is merged, unless the user explicitly wants the Goal workflow to
make the setup PR as its first checkpoint.

## Goal Issue Template

Use this structure:

````markdown
## Goal

<One sentence describing the end state.>

## Completion Contract

The Goal workflow should add `goal-completed` and remove `goal` only when:

- <Required condition 1>
- <Required condition 2>
- <Required condition 3>

## Evidence / Verification

<Commands, inline script, screenshots, logs, artifacts, or review checks that
prove the completion contract. Include exact expected outcomes.>

```bash
<optional inline doneness script>
```

## Scope and Constraints

The workflow may change:
- `<path or area>`

The workflow must not change:
- <protected behavior, API, dependency, data, or file>

## Context To Read First

- <files, docs, issues, PRs, logs, designs, references>

## Iteration Policy

Work in small checkpoints. After every run, report:
- what changed
- what was verified
- what remains
- whether anything is blocked

Prefer the smallest next checkpoint that can be validated with the evidence
above.

## Blocked Stop Condition

Stop substantive work and comment instead of guessing if:
- <missing secret, product decision, fixture, dependency, environment, or
  irreducible ambiguity>

The blocked comment should include the exact evidence gathered and the smallest
user action that would unblock the workflow.
````

## Quality Bar

Before creating or labelling the issue, check:

- Can another agent read the issue and know what to do first?
- Can the Goal workflow tell the difference between "done", "not done yet", and
  "blocked"?
- Is the verification evidence observable from the issue, the repo, a PR, or
  the workflow log?
- Are the constraints specific enough to prevent accidental broad rewrites?
- Is the goal one coherent objective?
- Is any setup PR genuinely necessary, or can the check live in the issue?

## GitHub Actions

If the repository has GitHub CLI available and authenticated, create the issue
with:

```bash
gh issue create --title "<short goal title>" --body-file /tmp/goal-issue.md --label goal
```

If you created a setup PR first, omit `--label goal` and tell the user to add
the label after the setup PR merges.
