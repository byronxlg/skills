# Orchestration

How the agent team is scheduled and run.

## Scheduling

| Role     | Interval |
| -------- | -------- |
| Director | 60m      |
| Lead     | 20m      |
| Builder  | 10m      |
| Reviewer | 10m      |

## Responsibilities

- Generate the runner script at `.claude/skills/orchestrator-ats/run-agents.sh`
- Configure `.claude/settings.json` with permissions agents need to run non-interactively
- Start, stop, and report status of agent cron jobs
- Detect and fix deadlocks (issues stuck in a state with no progress)
