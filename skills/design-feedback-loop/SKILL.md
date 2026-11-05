---
name: design-feedback-loop
description: Present design options to a human and collect their feedback through reactive, low-friction methods (try-on, duels, brackets, points budgets, sliders, drawing on the design, before/after wipes) instead of asking for written critique. Use whenever UI, page, screen or visual design work needs a person's taste in the loop - choosing between directions, tuning a layout, flagging what is off, or running a design review with several people. Also use when someone asks how to be shown options, how to get feedback on a design, or to "let me pick".
---

# Design feedback loop

Agents left to decide design on their own converge on a safe, bland average, and
verification cannot fix a weak direction. Put the human's taste at the decision
points: show options, let them pick and react, and turn that into the spec. This
skill covers how to present options and collect feedback with as little effort
from the human as possible.

It complements any planning or prototyping process you already follow (design guide,
prototypes, automated review); this skill covers the rounds where a human chooses and
reacts.

## Core principles

1. **Show the effect, never ask for an opinion in the abstract.** Every input should
   immediately change something the person can see. Methods that judge one idea in
   isolation, score something without changing it, or require typing performed
   poorly in testing.
2. **Recognition over articulation.** People are fast at recognising what is right and
   slow at describing it. Ask them to pick, tap, drag or mark, not to write.
3. **Silence means approve.** Anything they do not touch is accepted. Only ask for
   effort on what bothers them.
4. **Work per section or component, not whole pages.** Whole-page options bundle good
   and bad decisions together so they cannot be cleanly chosen. Let people mix
   ("header from B, cards from A").
5. **Force real divergence.** Give each generated option a different stance (dense and
   utilitarian, spacious and editorial, bold and playful). Otherwise you get three
   near-identical layouts.
6. **Use real content.** Render options with the actual copy and data, never lorem
   ipsum. Fake content makes everything look fine.
7. **One tap returns everything.** Picks, slider values, marks and notes go back in one
   structured payload. No copy-paste, no re-explaining.
8. **The chosen option becomes the spec.** Implement only once a direction is locked;
   verification then compares the build against that choice, not vague guidelines.

## Method catalogue

Ratings come from hands-on testing of each method on a real design task. Prefer the good methods.

### Good

| Method | What it is | Use it for |
| --- | --- | --- |
| Try-on | Tap any option and it drops straight into the live page; tap another to swap. | Picking between 2-4 options for a section. The default picker. |
| Duel | Two options side by side, tap the better one, repeat for the next decision. | Fast binary decisions (colour, size, style) in a short series. |
| Bracket | Duels arranged as semi-finals then a final. | Choosing among 4+ options without ranking a grid. |
| Points budget | Fixed budget (e.g. 16 points) spread across qualities such as Boldness, Whitespace, Detail; the page morphs as points move. | Tuning overall feel and forcing trade-offs. |
| Sliders | Continuous controls (headline size, spacing, accent strength) with a live preview. | Fine-tuning once structure is decided. |
| Vibe pad | Drag one point on a 2D pad (calm to energetic, minimal to rich); the whole page shifts. | A fast big-picture move. It bundles many changes, so offer per-section locks. |
| Before/after wipe | Drag a divider across the original and the current version. | Confirming a change was an improvement. |
| Draw on it | Red pen "fix this", green pen "love this", drawn on the preview; map each stroke to the section under it. | Flagging exactly where something is off or right. The most informative single method, but a red mark needs a follow-up duel or try-on to learn what is wrong. |
| Attention tracking | Time how long each option is in view while they scroll. No input needed. | Background signal to confirm picks or break ties. In testing it agreed with the explicit pick. |
| History scrubber | Scrub back through every version made this round, with restore. | Safety net that makes experimenting cheap. Always on. |
| Tap-to-edit section | Tap a section, then bigger or smaller, invert colours, move up or down, hide. | Structural tweaks without words. |

### Meh (avoid as primary methods)

| Method | Why it underperformed |
| --- | --- |
| Swipe deck (keep or skip single ideas) | Judges one idea in isolation, without seeing it combined with the rest. |
| Reaction scales (hate to love per section) | Asks for a score without changing anything visible. |
| Direct text editing | Typing on a phone is slow; it produces effort, not judgement. |

### Situational

- Quick chips under each section (too loud, more space, tighter, love this, cut it)
  plus an optional note: a lightweight fallback when sliders do not cover the issue.
- Voice notes: good for nuance, but speech capture is often blocked inside sandboxed
  previews; fall back to the keyboard's dictation into a text box.
- Slack buttons: post the comparison with pick buttons so a round takes seconds on a
  phone.

## Default flow

1. Diverge: 3-4 genuinely different directions for the overall look, as try-on or
   duels. No production code yet.
2. Structure: per-section try-on, with a bracket when a section has 4+ options.
3. Tune: points budget or sliders for overall feel, with a live preview.
4. Flag: draw on it for anything still wrong or worth protecting; follow up each red
   mark with a duel or try-on on that section.
5. Confirm: before/after wipe against the previous version.
6. Always running: history scrubber and attention tracking.
7. Build against the locked choices, then record what was picked and rejected (with
   reasons) in the project's design guide, so future first-round options start
   closer to the person's taste.

Keep each round to one screen of decisions. Lock earlier choices so they do not drift
in later rounds, and say in one line what the next round will be.

## Return payload

Every feedback surface sends back one structured message:

```
Round 3 tuning: headline 56px, spacing 23px, accent everywhere.
Picks: Focus areas = Numbered list, Career = Timeline.
Marks: 1x Career (fix), 1x Hero (love).
Attention: Timeline 17.5s, Cards 12.3s.
Note: <free text, if any>
```

Name sections the way the person sees them. Include only what changed or was flagged;
untouched items are implicitly approved.

## Where to render it

- **Chat with an inline visual tool** (a widget renderer with a `sendPrompt()` bridge):
  build each round as an interactive widget whose submit button calls
  `sendPrompt(payload)`. Lowest friction, works on mobile.
- **Claude Code on a real web app:** generate one local comparison page with the
  variants rendered from the actual components, and have it POST the payload to a
  small local endpoint or write a JSON file the session watches, so the next round
  starts without copy-paste. Screenshot variants with Playwright when options come
  from real branches.
- **Several reviewers:** a shared page where each reviewer's picks are stored per
  person, everyone's live picks and presence are visible, one reviewer can follow
  another's view, pins are shared with who left them, and one button hands the
  combined summary to the agent. Show disagreement per section ("Split" or "Agreed")
  rather than averaging it away.

## Anti-patterns

- Asking "what do you think?" or "any feedback?" in prose.
- Static images of options with no way to combine them.
- Whole-page A/B/C where every option changes everything.
- Making the person describe a problem in words before they can act on it.
- Implementing before the direction is locked.
- Making the person restate earlier choices each round.
