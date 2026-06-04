# Goal

Goal is an Agentic Workflow for GitHub issues.

It does something similar to `/goal` in Codex and Claude Code, packaged as a
variant of the Autoloop agentic workflow pattern.

Open an issue with the `goal` label and describe the outcome, completion
criteria, verification evidence, and constraints. Goal works on the issue across
runs using one long-running branch and PR. Each run comments on the issue. When
the goal is complete, it adds `goal-completed` and removes `goal`.

## Install

Paste this into your favorite coding agent to install Goal in your repo:

```text
Install the Goal Agentic Workflow using https://github.com/githubnext/goal/blob/main/install.md
```

## Use

1. Install Goal.
2. Open a GitHub issue with the `goal` label.
3. Make the definition of done concrete and verifiable.
4. Steer the work by commenting on the issue.
5. Review the long-running Goal PR when it is ready.
