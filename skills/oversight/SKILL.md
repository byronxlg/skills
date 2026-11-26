---
name: oversight
description: Set up or adjust a project's oversight calibration - the table in its runbook that says, for each kind of action an agent can take there, how bad a mistake would be and whether the agent acts alone, tells afterwards, asks first or hands off. Use when asked to "calibrate" a project, "set up oversight", "set up looprails", add or change a calibration row, loosen or tighten what agents may do in a repo, or when a project has agents acting with tools and no "Calibration" section in runbook/loops.md. Also use to review a calibration against what the project's runs actually did.
---

# Oversight calibration for a project

One project at a time. The calibration lives in the project, in the "Calibration" section of
`runbook/loops.md`, next to the code it governs. The global `oversight` rule sends every session
to that section before a shared-state action; this skill is how the section gets written and
changed. The method is LoopRails (looprails.dev/framework, Brenn Hill), in our own wording: its
kit is all rights reserved, so nothing is copied from it.

## The two scales

**Grade**: how bad if it goes wrong. The worst of undo, reach and stakes decides, and it is
graded by what really happens, not by what the tool promises. A shell delete has no undo. A sent
message is sent.

| Grade | Meaning | Examples |
| --- | --- | --- |
| G0 | read only; nothing outside the run changes | read a file, query a log |
| G1 | local and cheap to undo | edit in a worktree, a test run, a local commit |
| G2 | shared state, undone with effort | push, merge, restart, a config value, a message to the owner |
| G3 | cannot be taken back, or reaches other people | money, mail or posts to others, a delete, a credential, a deploy users see at once |

**Oversight**: what the owner sees, and when.

| Level | Meaning |
| --- | --- |
| O0 | act, nothing kept |
| O1 | act, kept in a log someone can audit |
| O2 | act, then say what was done and how to undo it |
| O3 | ask before the one action |
| O4 | the owner approves the plan; stops between steps |
| O5 | the owner decides first, before seeing a recommendation |
| O6 | do not act: hand off, or forbidden |

**Default pairing**: G0 at O0-O1, G1 at O1-O2, G2 at O3-O4, G3 at O4-O5, or O6 when a person
could not catch the mistake in time. Every project starts here. A request that names the action
is the yes for that action, in that context only.

## Set a project up

1. **Read what exists.** `runbook/loops.md` if present, the project's `CLAUDE.md` or `AGENTS.md`,
   its recovery runbook, CI and deploy workflows, and anything that records what the owner has
   already granted or forbidden there (a decisions log, an authority page, memory). Do not
   invent grants.
2. **List the actions an agent can take in this repo**, by what they touch: the repo (commit,
   push, merge), the running thing (restart, deploy, roll back, config), data (migrate, delete),
   the outside (mail, posts, payments, messages), keys. Include a session a person starts, not
   only scheduled loops. Leave out what the agent has no way to do.
3. **Grade each one** with the table above. Unsure means the higher grade.
4. **Start every row at the default.** Then mark a departure only where there is a recorded
   reason:
   - *Looser* (for instance a G2 restart at O2): only with the owner's yes. Quote the words and
     the date, or the decision that holds them. No record means the row stays at the default
     and goes on the list of questions in step 7.
   - *Tighter*: needs only a reason.
5. **Say what enforces each row.** A key the agent does not hold, a tool missing from its list,
   a branch protection or a cap in code is a control. An instruction is not; where that is all
   there is for a G3 row, say so and record the gap.
6. **Write the section.** If the project has no `runbook/loops.md`, create it with this section
   alone. Fleet projects use `templates/runbook/loops.md` from the management repo, which also
   carries loop cards, guards and signals for projects that run scheduled loops.

   ```markdown
   ## Calibration

   Default pairing: G0 at O0-O1, G1 at O1-O2, G2 at O3-O4, G3 at O4-O5, or O6 when a person
   could not catch the mistake in time. An action with no row below takes the default.

   | Action | Grade | Default | Here | Direction | Enforced by | Why | Granted |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | merge a green PR | G2 | O3-O4 | O2 | looser | CI required on main | revert PR is the undo | Byron, 2026-10-08, "you can merge freely" |
   | delete a table | G3 | O4-O5 | O6 | tighter | agent role has no DROP | no backup newer than a day | reason only |
   ```

   Only departures get a row. No departures: write "none" under the heading.
7. **Ask the owner once**, in plain words, about the rows that would save the most round-trips
   if loosened, worst grade last. One question per row, answerable yes or no. Record each yes
   in the row. Do not ask about G3 rows that are prevented by a control; they are not up for
   loosening by conversation.
8. **Open the PR in the project.** The calibration changes through the project's own PR flow, so
   its history sits with the code.

## Change a row

- **Tighter**: change it, give the reason, done.
- **Looser**: the owner's yes first, then the row, with the date and the words.
- **Propose looser** when the same ask-first question has been answered yes three times. Say
  the three occasions.
- **Propose tighter** (or just tighten) when an act-then-tell action had to be undone.
- A new action the agent can take, or a new tool or key in its reach, gets graded in the same
  PR that adds it.

## Review a calibration

Read the rows against what happened since the last review: which ask-first questions were asked
and how they were answered, which O2 actions were undone, any G3 attempt, any row whose
"Enforced by" is no longer true (a protection removed, a key widened). Update the `reviewed:`
date in the file's frontmatter. A calibration nobody has checked against real runs is a guess.
