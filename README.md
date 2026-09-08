# byronxlg-skills

Personal and adapted skills for Claude Code and Codex.

## Install with Skillfold

```bash
npm install -g skillfold
skillfold add -g github:byronxlg/skills/skills/obsidian
skillfold check -g
```

To use both agents, set `targets: [claude, codex]` in
`~/.config/skillfold/skillfold.yaml`, then run `skillfold install -g`. Skillfold 2.4.0+
can restrict an individual skill with `targets: [claude]` or `targets: [codex]`.

Byron's complete selection and exact source pins live in
[dotfiles](https://github.com/byronxlg/dotfiles), under `.config/skillfold/skillfold.yaml`
and `.config/skillfold/skillfold.lock`. Dotfiles installs Skillfold through npm and runs
`skillfold install -g --frozen`. Third-party skills are imported directly from
upstream rather than copied into this repository.

Edit personal skill sources here, commit and push, then update the consumer:

```bash
skillfold update -g obsidian
skillfold check -g
```

Commit the resulting dotfiles lockfile. Installed copies in `~/.claude/skills`
and `~/.agents/skills` are generated and should not be edited.

## Personal and adapted skills

| Skill | Purpose |
| --- | --- |
| `dbt` | Adapted dbt analytics workflow without MCP dependencies |
| `find-skills` | Discover skills and install them with Skillfold |
| `obsidian` | Work with Byron's Obsidian vaults |
| `polymarket` | Query markets and carry out explicitly requested trades |
| `tts` | Generate spoken audio |
| `issue` | Draft and create GitHub issues |
| `project-idea-validator` | Research and assess product ideas |

These were migrated from `byronxlg/dotfiles` at commit `206c3f0`.
`dbt` derives from dbt-labs/dbt-agent-skills, with the original author metadata
and Apache-2.0 license retained in its directory. Other third-party terms,
where supplied within a skill, take precedence over the repository license.

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
