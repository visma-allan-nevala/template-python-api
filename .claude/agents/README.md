# Code Review Agents

This folder contains LLM agent prompts for ensuring enterprise-grade code quality.
Use `orchestrator.md` to coordinate reviews.

## Quick Start

Before committing code, run a review:

```
Review Mode: changed
Agents: software_architect, cybersecurity_engineer, qa_test_engineer
```

## Available Agents

| Agent | Purpose |
|-------|---------|
| `orchestrator.md` | Coordinates multi-agent reviews |
| `software_architect.md` | Architecture and design review |
| `cybersecurity_engineer.md` | Security vulnerability review |
| `qa_test_engineer.md` | Test coverage and quality review |
| `performance_engineer.md` | Performance and scalability review |
| `data_privacy_engineer.md` | GDPR/privacy compliance review |
| `technical_writer.md` | Documentation review |
| `developer_experience.md` | Code readability and DX review |
| `error_handling_engineer.md` | Error handling patterns review |

## Review Modes

| Mode | Command | Use Case |
|------|---------|----------|
| `full` | Review entire codebase | Initial takeover, audits, pre-release |
| `changed` | Review git diff files | Pre-commit (default) |
| `staged` | Review staged files only | Final commit check |
| `branch` | Review branch vs main | PR reviews |

## Pre-Commit Review (Default)

Before creating any git commit, run the orchestrator with:

```
Review Mode: changed
Agents: software_architect, cybersecurity_engineer, qa_test_engineer
```

**Conditional Agents (add when applicable):**
- `data_privacy_engineer` - Changes touch personal data, user data, or logging
- `performance_engineer` - Changes touch hot paths, database queries, or algorithms
- `technical_writer` - Adding new public APIs, modules, or complex logic
- `developer_experience` - Significant new code or refactoring

## Severity Levels

- **CRITICAL/MUST FIX**: Must be resolved before committing
- **HIGH/SHOULD FIX**: Should be resolved before merging PR
- **MEDIUM/CONSIDER**: Optional improvements, document if deferring
- **LOW/OBSERVATION**: Nice to have, can be deferred

## Quick Review Mode

For small, low-risk changes (typos, config tweaks, minor fixes):

```
Review Mode: changed
Agents: software_architect, cybersecurity_engineer
```

## Agent Runs

The `runs/` folder stores execution logs from agent reviews.
These are gitignored to keep local review history private.
