# Skills and rules

Personal and adapted skills and rules for Claude Code and Codex, managed with
[Skillfold](https://github.com/byronxlg/skillfold).

## Available skills

| Skill | What it does | Example request |
| --- | --- | --- |
| [dbt](skills/dbt/SKILL.md) | Builds and changes dbt models, writes transformations and tests, diagnoses failures, and checks downstream impact. Adapted to work without MCP dependencies. | “Add a model for monthly revenue and validate the results.” |
| [find-skills](skills/find-skills/SKILL.md) | Searches GitHub and the web for existing skills, compares candidates, and installs selected skills with Skillfold. | “Find a skill for managing GitHub releases.” |
| [issue](skills/issue/SKILL.md) | Turns a request into a GitHub issue with background, requirements, and acceptance criteria. Shows the draft before creating it. | “Create an issue for adding CSV exports.” |
| [obsidian](skills/obsidian/SKILL.md) | Finds, creates, and edits Markdown notes across Byron's vaults while preserving frontmatter, wikilinks, and vault conventions. | “Find my project notes and update the next steps.” |
| [polymarket](skills/polymarket/SKILL.md) | Looks up prediction markets, prices, order books, positions, orders, and balances. Places or cancels trades only when explicitly requested. | “What are the markets saying about this event?” |
| [project-idea-validator](skills/project-idea-validator/SKILL.md) | Researches competitors and demand, challenges assumptions, and gives an evidence-backed go/no-go assessment with possible MVPs or pivots. | “Pressure-test this product idea before we build it.” |
| [tts](skills/tts/SKILL.md) | Converts text into spoken audio, with voice, speed, and tone controls, voice comparisons, and paragraph splitting. Uses the OpenAI audio API with credentials from Doppler. | “Read this script aloud and compare two voices.” |

Some skills use Byron's personal paths and credential conventions. Read the linked
instructions for prerequisites and supporting scripts before using them elsewhere.

## Available rules

Rules are always-on instructions, installed by Skillfold 2.6.0+ according to the
`rules` selection in the dotfiles manifest.

| Rule | What it does | Scope in Byron's config |
| --- | --- | --- |
| [communication-style](rules/communication-style.md) | Keeps writing concise and sets code, review, and formatting preferences. | Claude and Codex |
| [doppler](rules/doppler.md) | Discovers credentials through Doppler and reads secret notes before use. | Claude and Codex |
| [dotfiles-workflow](rules/dotfiles-workflow.md) | Stow ownership, Skillfold-managed skills and rules, and the commit-and-push requirement. | Claude and Codex |
| [infra-writes](rules/infra-writes.md) | Routes infrastructure changes through versioned code and GitHub Actions. | Claude and Codex |
| [kubectl-context](rules/kubectl-context.md) | Requires explicit Kubernetes and Helm contexts. | Claude and Codex |
| [tool-preferences](rules/tool-preferences.md) | Sets preferred command-line search and data-processing tools. | Claude and Codex |
| [project-notes](rules/project-notes.md) | Reads the Obsidian project note for the current repo before substantive work, if one exists. | Claude and Codex |
| [codex-compatibility](rules/codex-compatibility.md) | Adapts Claude skill examples and repository instructions for Codex. | Codex only |
| [doppler-secrets](rules/hosts/Byrons-Mac-mini/doppler-secrets.md) | Defines Doppler projects, credential scoping, and on-demand access. | Byrons-Mac-mini only |
| [telegram](rules/hosts/Byrons-Mac-mini/telegram.md) | Documents the personal Telegram notification channel. | Byrons-Mac-mini only |

Rules are behaviour only and short: `bin/check-rules` (CI) fails a rule over 12 non-blank lines unless `rules/.long-rules` names it with a reason. Facts go to the repo or fleet docs that own them; procedures become skills.

Declare a rule source in `~/.config/skillfold/skillfold.yaml`, then run
`skillfold install -g` and `skillfold check -g`:

```yaml
rules:
  doppler: github:byronxlg/skills/rules/doppler.md
  codex-compatibility:
    source: github:byronxlg/skills/rules/codex-compatibility.md
    targets: [codex]
  telegram:
    source: github:byronxlg/skills/rules/hosts/Byrons-Mac-mini/telegram.md
    hosts: [Byrons-Mac-mini]
```

Claude gets individual files under `~/.claude/rules/`; Codex gets a managed block
in `~/.codex/AGENTS.md`. Hostnames match exactly. All sources remain pinned in the
same lockfile; only matching rules are installed. Edit source rules here and push,
then run `skillfold update -g <rule-name>` and `skillfold check -g` and commit the
dotfiles lockfile. Do not edit generated instructions.

## Install with Skillfold

```sh
npm install -g skillfold
skillfold add -g github:byronxlg/skills/skills/obsidian
skillfold check -g
```

Replace `obsidian` with a directory name from the table. Omit `-g` to install for
the current project instead of your user account.

Skillfold 2.5.0+ keeps global configuration in
`~/.config/skillfold/skillfold.yaml` (or `$XDG_CONFIG_HOME/skillfold/skillfold.yaml`).
To install for both agents, set `targets: [claude, codex]` in that manifest and
run `skillfold install -g`. An individual skill can use a mapping with `source`
and `targets: [claude]` or `targets: [codex]` to restrict its destination.

Byron's selection and exact source pins live in
[dotfiles](https://github.com/byronxlg/dotfiles), under
`.config/skillfold/skillfold.yaml` and `.config/skillfold/skillfold.lock`.
Third-party skills are imported directly from upstream.

## Change a skill

Edit its source here, commit and push, then apply the change:

```sh
skillfold update -g obsidian
skillfold check -g
```

Commit and push the resulting dotfiles lockfile. `add`, `update`, and `remove`
already apply their changes. After editing the manifest directly, run
`skillfold install -g`; after pulling a changed manifest and lockfile, run
`skillfold install -g --frozen`.

Installed copies under `~/.claude/skills` and `~/.agents/skills` are generated.
Make changes in this repository rather than editing those copies.

## Attribution and license

These seven skills were migrated from `byronxlg/dotfiles` at commit `206c3f0`.
`dbt` derives from [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills),
with its author metadata and [Apache-2.0 license](skills/dbt/LICENSE) retained.

Original work is covered by the repository's [MIT license](LICENSE).
Third-party terms supplied within a skill take precedence for that material.
