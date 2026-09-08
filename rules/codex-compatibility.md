# Codex compatibility

When working in a repository that only has Claude instructions, read applicable `CLAUDE.md` files from the repository root down to the working directory. Prefer `AGENTS.md` where both exist at the same level.

Read `~/.claude/CLAUDE.md` if present for additional personal instructions. Shared and matching host rules are already included in this AGENTS.md by Skillfold; do not load `~/.claude/rules/` again.

## Shared skill compatibility

- Skillfold manages shared skills in `~/.agents/skills/` and `~/.claude/skills/` from `~/dotfiles/.config/skillfold/skillfold.yaml` and its lockfile. Installed copies are generated; do not edit them.
- Personal skill sources live in the `byronxlg/skills` repository. Edit and push sources there, then run `skillfold update -g <name>` and `skillfold check -g`. Commit and push the updated dotfiles lockfile.
- Add remote skills with `skillfold add -g <source>`; use per-skill `targets` for agent-specific skills.
- In shared skill examples, `/skill-name` means invoke the corresponding Codex skill with `$skill-name`; `$ARGUMENTS` means the user's request and conversation context, not a literal shell variable.
- Map Claude tool names to available Codex tools by capability. Claude `allowed-tools` metadata does not configure Codex permissions. Never assume a tool or connector exists just because a shared skill mentions it.
- Use Codex's installed document, spreadsheet, presentation, PDF, and skill-creator skills for those tasks. Claude-specific versions are not installed for Codex.
