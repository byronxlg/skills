---
name: agent-team-setup
description: Guides users through setting up an agent team from scratch - project definition, team design, orchestration - then generates all .claude specs. Use when the user wants to create a new agent team project.
---

# Agent Team Setup

Walk the user through setting up a complete agent team project, then generate all
the Claude specs from it.

## Commands

- **setup** (default) - walk through all phases to set up a new agent team from scratch
- **recompile** - regenerate all compiled artifacts (team rules, role skills, orchestrator skill) from existing spec files. Runs Phase 4 only.

If spec files already exist in `.claude/agent-team-setup-specs/`, ask the user whether
they want to make updates to the specs or recompile from what's there.

Templates for phases 1-3 are in `templates/`.

## Setup

Five phases, worked through in order. The first three phases produce definition files.
The fourth phase generates all Claude specs from them. The fifth phase sets up the
platform.

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
4. **Rules** - team-wide rules that apply to every role (coordination, boundaries, communication expectations)

Output: `.claude/agent-team-setup-specs/TEAM.md`

### Phase 3: Orchestration (how often does each role run?)

Walk the user through filling out an ORCHESTRATION.md file using the template in
`templates/ORCHESTRATION.md`.

Two sections:
1. **Scheduling** - define the interval for each role defined in TEAM.md. Offer a draft
   based on the roles' responsibilities - high-throughput roles (builders, reviewers)
   run more frequently, strategic roles (directors) run less often.
2. **Responsibilities** - what the orchestrator is responsible for beyond scheduling
   (e.g., deadlock detection, health checks)

Output: `.claude/agent-team-setup-specs/ORCHESTRATION.md`

### Phase 4: Generate (create all the specs)

Once the definition files are complete, generate all Claude specs in one step.
Read `.claude/agent-team-setup-specs/PROJECT.md`, `.claude/agent-team-setup-specs/TEAM.md`,
and `.claude/agent-team-setup-specs/ORCHESTRATION.md` as inputs.

Before generating, validate that all roles in ORCHESTRATION.md match roles in TEAM.md.
If they don't, stop and ask the user which spec to fix.

Use the platform mapping from PROJECT.md to translate abstract concepts into concrete
tool references in all generated files.

1. **`.claude/rules/team.md`** from TEAM.md:
   - Team rules that apply to every role (stay in your lane, one owner per work, etc.)

2. **`.claude/skills/{role}-ats/SKILL.md`** for each role in TEAM.md:
   - The role's purpose, before you start, priorities, outputs, and boundaries
   - The handoff transitions where this role is sender or receiver
   - The communication channels where this role posts or replies
   - Platform-specific commands and tools mapped from PROJECT.md (e.g., abstract "open a code review" becomes the concrete platform command)
   - The workflow states this role sets or works, as step-by-step instructions

3. **`.claude/skills/orchestrator-ats/SKILL.md`** from ORCHESTRATION.md + TEAM.md:
   - Reads the scheduling table from ORCHESTRATION.md for intervals
   - Reads the responsibilities from ORCHESTRATION.md for what the orchestrator does
   - Reads the role list from TEAM.md for role names; all skill commands follow the
     `/{name}-ats` naming convention - this applies to role skills (e.g., `/director-ats`,
     `/builder-ats`) and the orchestrator itself (`/orchestrator-ats`)
   - Reads the workflow states and handoffs from TEAM.md to understand expected state transitions
   - Generates the skill with commands derived from the responsibilities
   - Cron management must use system `crontab`, not Claude Code's session-scoped
     CronCreate/CronDelete tools (those expire after 3 days and only run within
     the Claude session)

All spec files live in `.claude/agent-team-setup-specs/` as source of truth. If something needs to
change, update the spec file and regenerate.

### Phase 5: Platform setup

Set up the tools agents need to interact with the platform, then configure the
platform itself.

**1. Platform tooling**

Based on the platform mapping from PROJECT.md, identify the CLI tool for the platform
(e.g., `gh` for GitHub). Then:

- Verify the CLI is installed and authenticated
- Use `/find-skills` to find and install a skill for that CLI (e.g., a `gh-cli` skill)
- Tell the user what was set up

If no CLI is available for the platform, suggest MCP as an alternative and help the
user configure it.

**2. Platform resources**

Using the CLI and the workflow/channels from TEAM.md, set up the platform:

- Create the project board with a column per workflow state
- Create discussion channels/categories matching the communication channels table
- Configure any other platform resources (labels, branch protection, etc.)

## Recompile

Delete all generated artifacts and regenerate from spec files:

1. Delete `.claude/rules/team.md`
2. Delete all `.claude/skills/{role}-ats/SKILL.md` files for roles defined in TEAM.md
3. Delete `.claude/skills/orchestrator-ats/SKILL.md`
4. Run Phase 4 (Generate) to recreate everything from the spec files
