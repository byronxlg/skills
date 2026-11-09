---
name: design-hitl
description: Run design decisions with a person in the loop - a web app, site, game or feature where the owner decides and the agent proposes, builds and records. Use whenever design or UX choices need someone's yes (a redesign, a UX pass, "give it a makeover", "who is this for", "let me try it"), when asking the owner design questions over chat or Telegram, or when a design change is about to go live. Covers the order of decisions (big to small, the user's job first), plain-words steps before pictures, one decision per message, try-it-live flags for UX, how to offer options, and recording answers. Works alongside the design-work rule and the taste skill, which cover how to make each design good.
---

# Design with a person in the loop

The owner decides; you propose, build, and record. They answer from a phone between other
things, so every question must be answerable in one look and one reply. Drawn from the
drift-foundry UX pass (2026-11-09), where this flow held up, and from earlier passes where it
did not (gyir thumbnails, ShoreWash, the drift-foundry design system). The examples come from a game; the
flow is for any web app, site or tool.

## 1. Agree the list of decisions first

Before any single screen, write the list of decisions in one file in the project
(`docs/ux/README.md` or similar), ordered big to small, and get a yes on the order.

- The first decision is the job: who comes to this, what they came to get done, and how they
  know they got it. One sentence each. For a booking app: a diner, a table for Friday, a
  confirmation they trust. For a dashboard: an owner, whether anything needs them today, a clear
  yes or no. Everything below depends on it, and screens drawn before it get redone.
- Then the main path, end to end, as the user walks it: arrive, do the job, leave with the
  result. Count the steps and name the one place people are most likely to stop.
- What the user does comes before how it looks: job, then path, then the other flows (first
  visit, empty, error, editing an earlier step, coming back), then layout, then visual detail.
- Each decision is judged against the job: does it make the job faster, clearer, or more
  trustworthy for that person? If no option changes that, it is a small decision; batch it.
- Keep a status column per decision (proposed / sent / set) and a progress line (done, now,
  left) for every message, so the owner never loses track of where the pass stands.
- When an answer reveals a bigger decision underneath ("who is this for?", "explain it from
  the top"), stop, add it above, and take it first. Do not keep drawing the smaller one.

## 2. Steps in plain words before any picture

For each decision, write how it works as numbered steps in plain words: what the user sees,
taps, and gets. Get a yes on the steps, then draw or build.

- No project jargon, engine terms, or internal names. If a term is needed, name it on a real
  screenshot first ("from the top"), then ask.
- Short. One sentence per step and per option. "Too much text" and "I don't understand" mean the
  message failed, not the owner.
- A mechanism is designed before the screen that shows it. If a look question turns out to be a
  mechanic, say so and design the mechanic first.

## 3. One decision per message

- Each message asks exactly one thing, answerable with a letter, yes, or a sentence.
- Options: as now, the simplest, and at most one more. Label A/B/C, mark your pick, and let the
  pick lean towards less. Say what each option changes, not how it is implemented.
- When the owner rejects the frame ("that is not what this is for", "stop about X, give me more options"),
  drop the frame entirely and come back with a wider spread (four or five), each meeting their
  stated test. Do not defend or re-pitch the old option.
- Reference products the owner names ("make it feel like X") are the brief: study what makes
  X work, say it in one line, and show how each option meets it.
- Reply in the thread the owner is answering; picture and question in the same message.

## 4. Pictures for the big decisions, something to try for UX

- Job, main-path, and look decisions: one picture per decision, made from the real product
  (real screenshots, real data, phone size), never a mock of an imagined screen. Put options
  side by side with "as now" first.
- Interaction and flow decisions: the owner has to try them. Build the steps behind a flag on
  the live product (`?ux=<n>`), send the link with the flag beside the link without it (as now),
  and ask yes or change after they have tried both. A picture of an interaction is not a
  decision anyone can make.
- Their first try usually finds something you did not ask about ("it automatically added the
  line"). Treat it as the next question: confirm what they saw, offer A/B, build the answer
  behind the same flag, and ask again.

## 5. Record, then apply

- Every answer goes into the decisions file the same run, verbatim with its date and message
  id, followed by what it means for the build. Commit through a PR.
- A yes on a flag means: make it the default, remove the flag, check it live on a phone, and
  say so in the reply.
- Nothing goes live until the owner has seen it and said yes in words. A juror score, a passing
  test, or silence is not a yes. "Give it a makeover" asks for a proposal, not a release.
- Settled decisions stay settled; do not reopen them unless the owner does.

## 6. Close the pass

When the list is done: one before/after of the whole product and a walk-through (video or
link), then ask for a final yes. Write what the pass taught about this flow back into this skill.

## Message shape

```
<project> <decision n>: <one-line question>
<picture or two links: as now / try it>
A. <plain sentence>  B. <plain sentence> (pick)  C. <plain sentence>
Done: 1, 3. Now: 4. Left: 5-9.
```

## Anti-patterns seen

- A form of many dropdowns with images elsewhere (gyir: "I'm a human not a bot").
- Option sheets full of mechanics the owner never learned (drift-foundry: "questions that I
  don't even understand").
- A screen drawn before the job was agreed, then redrawn twice.
- A design shipped live on a juror's win without the owner seeing it (ShoreWash, undone within
  the hour).
- Pictures sent for a UX decision that needed to be tried.
