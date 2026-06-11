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
| Last Run | 2026-06-11T22:02:19Z |
| Run Count | 1 |
| Completed | false |
| Completed Reason | - |
| Blocked | false |
| Blocked Reason | - |

## Current Checkpoint

- Added "Built On" section to README.md with links to Codex CLI /goal, Claude Code /goal, and Autoloop.
- All verification commands pass.
- Note: Claude Code `/goal` URL uses `https://code.claude.com/docs/en/slash-commands` — confirm this page exists (follows the pattern of known pages `/docs/en/overview`, `/docs/en/setup`, `/docs/en/data-usage`).

## Human Guidance

- Read new non-bot issue comments before every run.

## Evidence Log

- 2026-06-11T22:02:19Z: All four verification greps pass (autoloop, claude, codex, autoloop URL). Run https://github.com/githubnext/goal/actions/runs/27380112277

## Run History

- Run 1 (2026-06-11T22:02:19Z): Added Built On section, all greps pass, PR pending creation.
