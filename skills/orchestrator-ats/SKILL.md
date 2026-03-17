Base directory for this skill: /Users/byron/repos/agentlog

# Orchestrator

Manage the agent team cron jobs for agentlog.

## Commands

- **start** - start all agent cron jobs
- **stop** - stop all agent cron jobs
- **status** - show current cron job status and recent run history
- **restart** - stop then start all agent cron jobs
- **deadlock** - detect and report deadlocked issues (stuck in a state with no progress)

## Schedule

| Role | Interval | Skill command |
|------|----------|---------------|
| Director | 60m | /director |
| Lead | 20m | /lead |
| Builder | 10m | /builder |
| Reviewer | 10m | /reviewer |

## Runner script

The orchestrator generates and manages a runner script that invokes agents via
`claude` CLI. The script should:

- Invoke the correct skill command for each role
- Log output for debugging
- Use `--allowedTools` to restrict each role to its boundaries

## Cron management

Use system `crontab` for scheduling, not Claude Code's session-scoped CronCreate/CronDelete
tools (those expire after 3 days and only run within the Claude session).

### start

1. Generate the runner script if it doesn't exist
2. Add crontab entries for each role at its configured interval:
   ```
   # agentlog-director - every 60 minutes
   0 * * * * /path/to/runner.sh director >> /path/to/logs/director.log 2>&1
   # agentlog-lead - every 20 minutes
   */20 * * * * /path/to/runner.sh lead >> /path/to/logs/lead.log 2>&1
   # agentlog-builder - every 10 minutes
   */10 * * * * /path/to/runner.sh builder >> /path/to/logs/builder.log 2>&1
   # agentlog-reviewer - every 10 minutes
   */10 * * * * /path/to/runner.sh reviewer >> /path/to/logs/reviewer.log 2>&1
   ```
3. Verify crontab was updated

### stop

1. Remove all `agentlog-` prefixed entries from crontab
2. Verify removal

### status

1. Show current crontab entries for agentlog
2. Show recent log output for each role
3. Report any roles that haven't run recently

### restart

1. Run stop
2. Run start

### deadlock

Detect issues stuck in a workflow state with no progress:

1. Check the project board for issues that have been in the same state for too long
2. Look for:
   - **Ready** issues with no builder picking them up
   - **In Review** PRs with no reviewer activity
   - **Blocked** issues with no Lead response
   - **In Progress** issues with no commits or PR activity
3. Report findings and suggest actions

## Permissions

The orchestrator should ensure `.claude/settings.json` has the permissions agents
need to run non-interactively. This includes `gh` CLI commands, git operations,
and file system access.

## Responsibilities

- Generate the runner script for invoking agents
- Configure `.claude/settings.json` with permissions agents need to run non-interactively
- Start, stop, and report status of agent cron jobs
- Detect and fix deadlocks (issues stuck in a state with no progress)
