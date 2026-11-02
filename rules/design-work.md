# Design work: a positive idea, a written plan, prototypes, a blind juror

Any UI, page or screen work starts from a design idea, never from a defect list. Plan first, then build, in this order:

- Load the `taste` skill first (app screens: `references/app-screens.md`). Name the screen's one question and its one focal point per state. Write 5+ patterns borrowed from named good products in the same domain, each with what it changes on screen; the thing being sold gets a visual identity.
- Site-wide or "premium" asks need a design guide before any screen: palette as named roles (ground, ink, accent, meal or category colours) with contrast checked, type scale, spacing, radii, elevation, motion, and the taste `tells.md` list as banned patterns. Commit it as tokens plus a doc, and apply it to every page, not only the one in hand.
- Stateful flows (chat, checkout, multi-step) need a state map before layout: every state, every action a user can take from it (back, edit an earlier step, click a stale item, reload, error, empty), and the way forward from each. No dead ends; each row becomes a browser test.
- Get an independent review of the guide and the state map before prototyping; fix what it finds.
- Build two genuinely different directions as static prototypes with real data; screenshot phone and desktop; look at every shot yourself before anyone else does.
- Judge with a blind juror: a fresh agent sees the before and the candidates unlabelled, against named reference products, and walks the state map. Ship the winner only if it beats the before, after fixing the juror's top defects.
- Subtraction is not a design pass: removing boxes or merging text styles must come with added hierarchy (size and weight contrast, grouping by region, a focal point).
- A screen is done when its screenshots say so, for every page the change touches, never from tests or code review alone.
- Why: ptt, 2026-11-02. Three subtractive passes left a wall of same-weight grey text; then the site had no shared palette and the chat had dead ends nobody had mapped.
