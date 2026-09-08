Claude Code config (`settings.json`, agents, hooks, statusline) and other dotfiles (`.config/`, `.vscode/`, `.zshrc`, `.zshenv`, `.tmux.conf`) are symlinked from `~/dotfiles` via GNU Stow.

Skills and rules are managed by Skillfold from `byronxlg/skills` and upstream sources. Their manifest and lockfile are Stow-managed in `~/dotfiles/.config/skillfold/`; installed skill directories, `~/.claude/rules/`, and `~/.codex/AGENTS.md` are generated. Follow `skills.md` to change and apply them.

- Edit these files in `~/dotfiles/`, not directly in `$HOME`
- Run `stow . --no-folding` from `~/dotfiles` after changes
- Always commit and push dotfiles changes made for the task before considering the work complete. This includes config, rules, skills, and agent instructions. Do not wait for a separate request to commit or push.
- Stage only the task's changes; preserve unrelated existing edits. Verify the staged diff, commit, push to the remote, and confirm the push completed. If committing or pushing is blocked, report the blocker explicitly.
- Claude Code secrets (API keys, Bedrock creds, etc.) live in `~/.zshenv.local`, gitignored and outside this repo. `~/.claude/settings.json` itself is stow-managed and free of secrets.
