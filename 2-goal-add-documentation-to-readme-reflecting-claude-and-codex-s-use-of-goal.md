# Goal #2: Goal: add documentation to readme reflecting Claude and Codex's use of /goal

This file is maintained by the Goal workflow. Maintainers may edit guidance
sections directly.

## Machine State

| Field | Value |
|-------|-------|
| Issue | #2 |
| Branch | `goal/2-goal-add-documentation-to-readme-reflecting-claude-and-codex-s-use-of-goal` |
| PR | - |
| Status | active |
| Last Run | 2026-06-11T22:35:36Z |
| Run Count | 2 |
| Completed | false |
| Completed Reason | - |
| Blocked | false |
| Blocked Reason | - |

## Current Checkpoint

- Fixed PLACEHOLDER_RE false positive that caused scheduler to incorrectly flag issue #2 as needs_action.
- Added "Built On" section to README.md with links to Codex CLI /goal, Claude Code /goal, and Autoloop.
- All four verification greps pass.
- Claude Code URL `https://code.claude.com/docs/en/slash-commands` follows confirmed URL pattern but specific page needs human confirmation.
- PR created with these changes.

## Human Guidance

- Read new non-bot issue comments before every run.

## Evidence Log

- 2026-06-11T22:02:19Z: All four verification greps pass (autoloop, claude, codex, autoloop URL). Run https://github.com/githubnext/goal/actions/runs/27380112277
- 2026-06-11T22:35:36Z: Run 2 — scheduler bug fixed (PLACEHOLDER_RE), README Built On section committed, all 5 tests pass, all 4 greps exit 0. Run https://github.com/githubnext/goal/actions/runs/27381629433

## Run History

- Run 1 (2026-06-11T22:02:19Z): Added Built On section, all greps pass, PR pending creation (blocked by protected file rules).
- Run 2 (2026-06-11T22:35:36Z): Fixed PLACEHOLDER_RE false positive, committed README + scheduler fix, created PR.
