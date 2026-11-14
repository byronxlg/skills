# Building apps: own a thin layer on primitives

When an app needs a chart, form flow, data grid, editor or similar, decide between a high-level library and primitives by how far the requirement sits from the library's defaults. An agent writes the layer in minutes, so the old default of "highest abstraction available" no longer holds.

- **Ask of every dependency**: does it compute something, or decide something? Keep the ones that compute (d3-scale and d3-shape, date-fns, zod, floating-ui, SQL, plain SVG and DOM). Be wary of the ones that decide rendering, styling, animation and interaction (`<BarChart>`-style kits), because those carry the product's identity.
- **Custom look or behaviour** (must match a design system, bespoke interaction, a second workaround already needed): build a few hundred lines on primitives, in the project's own tokens and component API, in a folder the project owns.
- **Commodity UI** (internal dashboard, default styling is fine): use the library and stay on its defaults. Rebuilding it is vanity.
- **Never hand-roll hard, stable problems**: date arithmetic, colour interpolation, schema validation, floating positioning, and accessible widgets (combobox, date picker, modal focus). Use the mature library; headless ones keep the look yours.
- **Spike before committing** when unsure: an hour on each side behind the same component API, then keep the side with fewer workarounds. An installed library is not a reason to use it.
- **Owning it means maintaining it**: only build what you can judge (say what each primitive does before using it), write the layer's pattern into the project docs, and cover it with tests and screenshots, or it becomes a liability.
- Why: Robin Wieruch, "Agentic Coding: Bet on the Primitives" (2026-07-31, robinwieruch.de/agentic-coding-bet-on-primitives). D3 plus React SVG matched a client's design fully; Recharts got 80% fast, then needed the same custom SVG and its entrance animation froze.
