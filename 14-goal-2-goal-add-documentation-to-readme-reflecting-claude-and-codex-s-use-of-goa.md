# Goal #14: [Goal #2] Goal: add documentation to readme reflecting Claude and Codex's use of /goal

This file is maintained by the Goal workflow.

## Machine State

| Field | Value |
|-------|-------|
| Issue | #14 |
| Branch | `goal/14-goal-2-goal-add-documentation-to-readme-reflecting-claude-and-codex-s-use-of-goa` |
| PR | - |
| Status | needs_action |
| Last Run | 2026-06-14T14:08:54Z |
| Run Count | 6 |
| Completed | false |
| Blocked | false |

## Current Checkpoint

Waiting for missing sections: completion_contract, scope, iteration_policy, blocked_stop_condition.

## Evidence Log

- Runs 1–6: needs_action; missing 4 of 6 required sections. No human response after 6 runs.

## Requested Clarifications

1. **Completion Contract** — what exact state of README.md satisfies the goal?  
   Draft: "README.md contains a `Built On` section with links to Autoloop, Claude Code /goal docs, and Codex /goal docs; all grep checks pass; scheduler tests pass."
2. **Scope and Constraints** — which files may be changed? Is the PLACEHOLDER_RE scheduler fix in scope?  
   Draft: "Only README.md. The scheduler fix is a separate concern and should be a separate issue."
3. **Iteration Policy** — how should work proceed across runs?  
   Draft: "Each run verifies grep evidence, updates PR body with latest URL confirmations. Blocked if Claude URL cannot be confirmed."
4. **Blocked Stop Condition** — when to stop rather than guess?  
   Draft: "Stop if the Claude Code /goal URL cannot be confirmed after human review."
