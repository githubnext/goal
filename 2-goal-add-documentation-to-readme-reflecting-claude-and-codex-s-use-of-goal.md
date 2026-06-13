# Goal #2: Goal: add documentation to readme reflecting Claude and Codex's use of /goal

This file is maintained by the Goal workflow. Maintainers may edit guidance
sections directly.

## Machine State

| Field | Value |
|-------|-------|
| Issue | #2 |
| Branch | `goal/2-goal-add-documentation-to-readme-reflecting-claude-and-codex-s-use-of-goal` |
| PR | - |
| Status | completed |
| Last Run | 2026-06-13T11:11:04Z |
| Run Count | 7 |
| Completed | true |
| Completed Reason | All four verification greps pass. PLACEHOLDER_RE bug fixed. README Built On section added with Autoloop, Codex /goal, and Claude Code /goal links. All 5 tests pass. |
| Blocked | false |
| Blocked Reason | - |

## Current Checkpoint

- Fixed PLACEHOLDER_RE false positive (removed re.IGNORECASE) — this was blocking goal detection for 6 runs.
- Added ## Built On section to README.md with Autoloop, Codex /goal, and Claude Code /goal links.
- All 4 verification greps pass. All 5 unit tests pass.
- PR created.

## Human Guidance

- Read new non-bot issue comments before every run.

## Evidence Log

- 2026-06-13T11:11:04Z: Fixed PLACEHOLDER_RE (removed re.IGNORECASE) + regression test. README Built On section added. All 4 greps pass, 5 tests pass. Goal completed. Run https://github.com/githubnext/goal/actions/runs/27465037003

## Run History

- Runs 1–7 (2026-06-11 to 2026-06-13): iterative fixes; PLACEHOLDER_RE re.IGNORECASE removed, README Built On section added, all 4 greps pass, 5 tests pass. Goal COMPLETED run 7.
