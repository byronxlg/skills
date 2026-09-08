# Skills

Personal and adapted skills for Claude Code and Codex, managed with
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
