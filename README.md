# Goal

Goal turns a GitHub issue into a durable agentic workflow. Open an issue with the
`goal` label, define what "done" means, and the workflow keeps working on the
same branch and pull request until the evidence satisfies the goal. When it is
done, the workflow adds `goal-completed` and removes `goal`.

Goal runs on [GitHub Agentic Workflows](https://github.github.com/gh-aw/setup/quick-start/)
and [GitHub Copilot](https://github.com/features/copilot).

## Quick Start

Paste this into your favorite coding agent session on the repo where you want to
run Goal:

```text
Install goal using https://github.com/githubnext/goal/blob/main/install.md
```

The agent will install GitHub Agentic Workflows if needed, copy the Goal
workflow, compile it, create labels and issue templates, and help you turn your
first rough idea into a concrete goal issue.

## How It Works

1. Create a GitHub issue with the `goal` label.
2. Describe the outcome, completion contract, verification evidence, scope, and
   blocked stop condition.
3. On each scheduled run, Goal selects one active issue, reads the issue and new
   comments, and advances the work on the canonical branch `goal/<issue>-<slug>`.
4. The workflow keeps exactly one draft PR for that issue and updates the PR body
   as evidence changes.
5. Every run posts a new comment on the goal issue and updates a status comment.
6. When the completion contract is satisfied by concrete evidence, Goal comments
   with the evidence, adds `goal-completed`, and removes `goal`.

Goal stores durable state in repo-memory on the `memory/goal` branch. The state
file records the issue, branch, PR, last run, current checkpoint, lessons,
blockers, and run history. Humans can edit the issue or comment with steering;
the next run treats that input as part of the active contract.

## Goal Issues

A good goal issue is a compact contract, not a vague backlog item. It should
answer:

- **Outcome**: what should be true when the work is done.
- **Evidence**: which commands, tests, files, screenshots, logs, or artifacts
  prove the outcome.
- **Constraints**: what must not change, regress, or be modified.
- **Boundaries**: which files, tools, services, or data the workflow may use.
- **Iteration policy**: how the agent should choose the next action after each
  run.
- **Blocked stop condition**: when the workflow should stop substantive work and
  report what would unlock progress.

Use the included issue template, or write the sections directly:

````markdown
## Goal

Ship the new checkout retry path.

## Completion Contract

The retry path is implemented, old checkout behavior still passes its tests, and
the issue can be closed when the commands below pass on the PR branch.

## Evidence / Verification

```bash
npm test -- checkout
npm run lint
```

## Scope and Constraints

Allowed files:
- `src/checkout/**`
- `tests/checkout/**`

Do not change public API names or payment provider configuration.

## Iteration Policy

Prefer the smallest checkpoint that can be verified in one run. Read new human
comments before choosing the next checkpoint.

## Blocked Stop Condition

If the tests require credentials or fixtures unavailable to the workflow, stop
and comment with the missing item and the smallest reproducible evidence.
````

## Branches And PRs

Each goal issue owns one long-running branch:

```text
goal/<issue-number>-<slugified-title>
```

Examples:

- `goal/42-fix-checkout-retry`
- `goal/108-migrate-auth-tests`

Goal always reuses the same branch and the same draft PR for an issue. It never
creates per-run branch suffixes, run IDs, or random tokens.

## Repository Structure

```text
goal/
|-- install.md
|-- workflows/
|   |-- goal.md
|   |-- scripts/
|   |   `-- goal_scheduler.py
|   `-- shared/
|       `-- reporting.md
|-- .github/
|   `-- ISSUE_TEMPLATE/
|       `-- goal.md
`-- tests/
    `-- test_goal_scheduler.py
```

## Built On

- [GitHub Agentic Workflows](https://github.com/github/gh-aw)
- [GitHub Copilot](https://github.com/features/copilot)
- Goal-command ideas from Codex and Claude Code: durable objectives, explicit
  evidence, scoped continuation, and evidence-based completion.
