Claude Code config (`settings.json`, agents, hooks, statusline) and other dotfiles (`.config/`, `.vscode/`, `.zshrc`, `.zshenv`, `.tmux.conf`) are symlinked from `~/dotfiles` via GNU Stow. Edit them in `~/dotfiles/`, never in `$HOME`, then `stow . --no-folding` from `~/dotfiles`.

Skills and rules are Skillfold-managed. Sources live in `byronxlg/skills` (personal) or upstream repos; the manifest and lockfile are Stow-managed in `~/dotfiles/.config/skillfold/`; everything installed (`~/.claude/skills`, `~/.agents/skills`, `~/.claude/rules`, the managed block in `~/.codex/AGENTS.md`) is generated and never edited by hand. Change the source, then `skillfold add|update|install -g`, finish with `skillfold check -g`. `skillfold --help` for the rest.

- Commit and push the task's dotfiles changes (config, manifest, lock) before calling the work complete; stage only the task's changes and confirm the push.
- Secrets for Claude Code live in `~/.zshenv.local`, gitignored and outside the repo; `settings.json` stays free of secrets.
