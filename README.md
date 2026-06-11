# Goal

Goal is an Agentic Workflow for GitHub issues.

It does something similar to `/goal` in Codex and Claude Code, packaged as a
variant of the Autoloop agentic workflow pattern.

Use an agent to create a good goal issue, and sometimes a small setup PR, before
the workflow starts. Goal then works on that issue across runs using one
long-running branch and PR. Each run comments on the issue. When the goal is
complete, it adds `goal-completed` and removes `goal`.

## Install

Paste this into your favorite coding agent to install Goal in your repo:

```text
Install the Goal Agentic Workflow using https://github.com/githubnext/goal/blob/main/install.md
```

## Use

Paste this into your favorite coding agent to create a good goal:

```text
Install the Goal Agentic Workflow using https://github.com/githubnext/goal/blob/main/new-goal.md
```

The agent should help turn the work into a concrete, verifiable issue before
the `goal` label is added.
