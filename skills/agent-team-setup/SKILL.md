---
name: agent-team-setup
description: Guides users through setting up an agent team from scratch - project definition, team design - then generates all .claude specs. Use when the user wants to create a new agent team project.
---

# Agent Team Setup

Walk the user through setting up a complete agent team project, then generate all
the Claude specs from it.

## When to use

When the user wants to create a new agent team project from scratch, or regenerate
specs from existing definition files.

## How it works

Four phases, worked through in order. The first two phases produce definition files.
The third phase generates all Claude specs from them. The fourth phase sets up the
platform.

Templates for phases 1 and 2 are in `templates/`.

### Phase 1: Project (what are we building?)

Walk the user through filling out a PROJECT.md file using the template in
`templates/PROJECT.md`.

Two sections:
1. **Identity** - name, repo, description, tech stack
2. **Platform** - map abstract team concepts (issues, code reviews, discussion channels, etc.) to concrete tools

Keep it minimal. Offer a draft for the user to react to.

Output: `.claude/agent-team-setup-specs/PROJECT.md`

### Phase 2: Team (who does what?)

Walk the user through filling out a TEAM.md file using the template in
`templates/TEAM.md`. Work through each section in order, offering a first draft
for the user to react to rather than asking open-ended questions.

The sections, in order:

1. **Roles** - for each role, define:
   - Purpose (one line - why it exists)
   - Before you start (context to gather before doing any work)
   - Priorities (ordered priority stack - work the highest applicable first)
   - Outputs (what this role produces)
   - Boundaries (what this role must never do)
2. **Workflow** - states with Set by (who moves work into this state) and Worked by (who does work in this state)
3. **Handoffs** - transition table (from -> to, triggered by, artifact, preconditions) plus communication channels (channel, post type, posted by, thread, purpose)

Output: `.claude/agent-team-setup-specs/TEAM.md`

### Phase 3: Generate (create all the specs)

Once the definition files are complete, generate all Claude specs in one step.
Read `.claude/agent-team-setup-specs/PROJECT.md` and `.claude/agent-team-setup-specs/TEAM.md`
as inputs. Use the platform mapping from PROJECT.md to translate abstract concepts into
concrete tool references in all generated files.

1. **CLAUDE.md** from PROJECT.md + TEAM.md:
   - Project name and description
   - Tech stack
   - Team roles summary (role name + purpose, one line each)
   - Workflow state table
   - List of available skills

2. **`.claude/skills/{role}-ats/SKILL.md`** for each role in TEAM.md:
   - The role's purpose, before you start, priorities, outputs, and boundaries
   - The handoff transitions where this role is sender or receiver
   - The communication channels where this role posts or replies
   - Platform-specific commands and tools mapped from PROJECT.md (e.g., abstract "open a code review" becomes the concrete platform command)
   - The workflow states this role sets or works, as step-by-step instructions

All spec files live in `.claude/agent-team-setup-specs/` as source of truth. If something needs to
change, update the spec file and regenerate.

### Phase 4: Platform setup

Using the platform mapping from PROJECT.md and the workflow/channels from TEAM.md,
set up the platform:

- Create the project board with a column per workflow state
- Create discussion channels/categories matching the communication channels table
- Configure any other platform resources (labels, branch protection, etc.)
- Use platform-specific commands mapped from PROJECT.md
