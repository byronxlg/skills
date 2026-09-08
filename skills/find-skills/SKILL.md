---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
allowed-tools: Bash(gh search *), Bash(gh api *), Bash(gh repo *), Bash(curl *), Bash(skillfold *), WebSearch
model: sonnet
---

# Find Skills

This skill searches for ready-made SKILL.md files and installs them locally.

Skills are managed by Skillfold. The global manifest in `~/dotfiles/.claude/skillfold.yaml` selects skills for Claude and Codex; installed copies are generated. Search uses GitHub code search and web search.

## How to find skills

### Step 1: Search both paths in parallel

**GitHub code search:**
```bash
gh search code --filename SKILL.md "<query>" --json repository,path,url --limit 20
```

**Web search:**
```
site:github.com SKILL.md "<query>" claude code skill
```

Combine results across both paths. Deduplicate by `owner/repo + path` — if the same file appears from both searches, keep one entry.

### Step 2: Filter out aggregators and mirrors

Before fetching content, discard obvious junk:
- Repos whose name or description suggests they are aggregators, mirrors, or scrapers (e.g. `skills_feed`, `awesome-claude-skills`, `claude-skill-registry`, `skills-md`)
- Repos that appear multiple times with identical descriptions but different owners - keep only the one with the most stars

Fetch star counts for surviving candidates:
```bash
gh repo view <owner/repo> --json stargazerCount,description,isFork
```

Prefer repos that are not forks. Treat star counts as a rough quality signal: 500+ is a good sign, under 50 is worth noting to the user. Deprioritize but don't discard low-star repos from unknown authors — surface them at the bottom of the list with a note.

### Step 3: Fetch SKILL.md content

For each candidate, compute the raw URL by replacing `github.com` with `raw.githubusercontent.com` and dropping `/blob`:

```
https://github.com/<owner>/<repo>/blob/<sha>/<path>
->
https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<path>
```

The SHA is preserved as-is — do not substitute `main` or any branch name.

Fetch the content and check it is non-empty before proceeding:
```bash
content=$(curl -sfL "<raw-url>")
# abort this candidate if content is empty or curl failed
```

Extract the `description:` field from the YAML frontmatter of non-empty results.

### Step 4: Present options

Show the user a ranked list (higher stars first within each quality tier):
- Skill name (last directory component before SKILL.md)
- Description (from frontmatter)
- Source repo and star count
- GitHub URL

Example:
```
gog (steipete/clawdis, 2.1k stars)
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.
https://github.com/steipete/clawdis/tree/main/skills/gog
```

### Step 5: Install

When installation is requested, use the skill directory as the source so supporting
scripts and references are installed too:

```bash
skillfold add -g github:<owner>/<repo>/<skill-directory> --name <name>
skillfold check -g
```

Use an `@<sha>` suffix when the user selected that exact revision. For a project-only
skill, omit `-g` and run from the project root. Preserve existing names; resolve a
conflict with the user when their intended replacement is unclear.

Skills inherit the manifest's targets. For an agent-specific skill, declare a mapping
with `source` and `targets: [claude]` or `targets: [codex]` in the manifest before
running `skillfold install -g`. This requires Skillfold 2.4.0 or later.

Global manifests and lockfiles are Stow-managed dotfiles. Edit their repository
sources, run `stow . --no-folding`, and commit and push the task's manifest and lock
changes. Personal skill sources belong in `byronxlg/skills`; update and push the
source there, then run `skillfold update -g <name>` and `skillfold check -g`.

## Listing installed skills

```bash
skillfold list -g
skillfold info -g <name>
```

## When nothing is found

Say so clearly and offer to create a new skill with the `skill-creator` skill.
