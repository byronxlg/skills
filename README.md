# byronxlg-skills

A collection of Claude Code skills by byronxlg.

## Install

```bash
claude plugin add byronxlg/skills
```

Or via the [agent-skills-cli](https://www.npmjs.com/package/agent-skills-cli):

```bash
npm install -g agent-skills-cli
skills install byronxlg/skills
```

## Skills

### Agent Team

A framework for creating and managing teams of Claude Code agents with defined roles, workflows, and coordination rules.

| Skill | Description |
|-------|-------------|
| `/agent-team-setup` | Walk through setting up a new agent team project from scratch |
| `/director` | Act as the Director - vision, strategy, priorities, business blog posts |
| `/lead` | Act as the Lead - triage, create issues, manage the board, technical blog posts |
| `/builder` | Act as the Builder - implement issues, write tests, open PRs |
| `/reviewer` | Act as the Reviewer - review PRs against acceptance criteria |

## License

MIT
