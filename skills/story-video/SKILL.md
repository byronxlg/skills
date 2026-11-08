---
name: story-video
description: Make a short story-driven video (product demo, pitch, hackathon or launch video) as an HTML + GSAP composition rendered to MP4 with HyperFrames. Covers planning the story, building scenes, verifying stills, rendering, poster frames and iterating on feedback. Use when someone asks for a demo video, pitch video, explainer, ad-style video or "brag" video of something they built.
---

# Story video

Build the video as one HTML page whose animation runs on a single paused GSAP timeline. HyperFrames seeks that timeline frame by frame and renders it to MP4. Every frame is deterministic, so you can check any moment as a still before you render.

**Needs:** Node 20+ (for `npx hyperframes`), ffmpeg/ffprobe, a copy of `gsap.min.js` (from the `gsap` npm package or cdnjs), a `.woff2` font, and any music and SFX you have the rights to use.

Workflow: **plan → storyboard → compose → check → stills → render → poster → share → iterate.**

## 1. Plan before you build

Write `<out>/plan.md` first. Answer these:

- **Audience.** Who watches it, and what should they think or do afterwards? A judging panel, a team, customers and executives each need a different video.
- **One-line message.** The thing a viewer should repeat after one viewing.
- **Hero.** Whose story is this? Usually the end user, not the system. Show the system's steps at a high level only if the audience needs to see how it works.
- **Evidence.** Real numbers, quotes and examples, each with a source. Keep a list of claims and where each comes from.
- **Criteria.** If the video is judged, list the criteria and map every scene to at least one.
- **Length.** Decide it up front. Social cut: 15–30s. Demo or pitch: 60–120s. Respect any hard limit.

Then write a storyboard table: `# | time | scene | on-screen text | what moves | why it's here`. A common shape:

```
Hook (customer moment) → Problem (evidence) → Before vs after → Reveal (name it)
→ How it works (3–5 steps, real example) → Payoff (the outcome) → What changes / readiness → Outro (name + team)
```

**Honesty rules.** These matter more than polish:

- Use only claims you can source. If a stat or behaviour isn't real, cut it.
- Track staged or replayed content ("recorded run", "prototype on sample data", "target design") in `plan.md` and the delivery message, not on screen. Footnotes, source lines and "illustrative" labels clutter the frame; add them to the video only if the user asks.
- Don't show capabilities the product doesn't have yet as if they work. Leave them out, or show them as "next" if the user wants them in.
- Before you share, list for the user every place where the video goes beyond what the real thing does today.

**Examples.** A made-up example must make its point at a glance. If it is meant to show a failure, a viewer with no context should see that it's wrong; ask "could this pass as a correct answer?" When the client or brand must stay anonymous, check the example's topic, product nouns and team names for hints, not just the obvious names.

**Show product features the way the product does.** When you recreate a product's screen or graphic, keep the form the real product uses (a tree stays a tree, a chart stays a chart). Render it from the product's own code or assets where you can.

## 2. Project layout

```
<out>/
  plan.md
  composition/
    index.html        # the video
    assets/           # local copies only: gsap.min.js, font .woff2, music, sfx, images
  work/               # renders, snapshots, backups (not shared)
  video.mp4           # final, with poster baked in as frame 0
  poster.jpg
  share-copy.txt      # 2–4 sentence caption for posting
  v1/, v2/ ...        # frozen copies of earlier versions
```

Keep every asset local. Renders must not depend on the network. Copy `gsap.min.js` into `assets/`, and self-host the font with `@font-face` and `font-display: block`.

Start from `templates/index.html` in this skill. It has the scaffold, the helpers, and an example of each common technique.

## 3. Composition rules (HyperFrames)

- The root is `<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="N">`.
- Each scene is `<section class="clip" data-start="S" data-duration="D" data-track-index="1">`. Scenes on the same track must not overlap.
- Animate with **one** `gsap.timeline({ paused: true })` at absolute times, and register it with `window.__timelines["main"] = tl`. Don't use `setTimeout`, CSS animations, `Date.now()`, or `Math.random()` without a seed.
- Audio is `<audio>` with `data-start`, `data-duration`, `data-volume` and a **unique** `data-track-index` per element. For fades, use `data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0.6},{"t":1.5,"v":1},{"t":N-2.5,"v":1},{"t":N,"v":0}]}]}'`.
- **Animate transforms and opacity only** (`x`, `y`, `scale`, `rotation`, `opacity`). The linter flags tweens on `left`/`top`/`width`/`height`. To morph one box into another, use `scaleX`/`scaleY` with `transformOrigin: "0 0"`, then cross-fade to the real target element.
- To typing-animate text, split it into `<span>` per character and toggle `display: none → inline` at timed offsets. Don't toggle opacity: hidden characters still take up width, and the caret ends up in the wrong place.
- To show a click, tween the cursor to the target and arrive exactly at the click time. Then do a quick `scale: 0.92 → 1` on the button, change its colour, and play a click SFX at the same time.
- Use one `out(selectors, t)` helper for scene exits, and a consistent ease (`power3.out` in, `power2.in` out).
- Write every timeline position as a decimal (`106.0`, not `106`). `shift_timeline.py` moves only decimal numbers, so an integer time silently stays put. Don't mass-convert integers to fix this, because offsets and sizes would shift too.
- To move something along a drawn line or curve, sample that path's actual geometry (e.g. the SVG path's Bézier segments) into keyframes. Don't keyframe straight lines between a few points. Check it with `snapshot --range` along the path.

## 4. Readability (most common feedback)

- Text a viewer must read stays on screen long enough: about **0.3s per word**, plus about 1s, after it settles. Short labels need at least 0.8s.
- Animate in fast, then hold. Never animate in fast and then cut away.
- Use a minimum of 20px for small labels at 1080p, and 26px or more for anything that matters. Headings are 56–72px.
- A heading that promises items ("Two questions…", "Three steps…") must show those items on screen, in the same scene or the next one.
- Keep a contrast ratio of 4.5:1 for body text and 3:1 for large text. `hyperframes check` reports failures. Don't put white text on a light brand colour; use the darker shade.
- If the user says it's too fast, offer a uniform slowdown that keeps everything else the same (see 8), or retime to longer holds.

## 5. Check, then look at stills

Run from `composition/`:

```bash
npx hyperframes check                     # lint, layout, motion, contrast: 0 errors required
npx hyperframes snapshot --at 4.0,12.5,41.0 --no-end -o ../work/snap .
```

Then **look at the snapshots** (`contact-sheet.jpg`, and individual frames at full size for detail). Check:

- **Clicks.** Snapshot at the exact click time. The cursor tip should sit on the button, not just near it. The tip is offset from the cursor element's origin, so adjust and re-snapshot.
- **Overlaps.** Card heights are usually larger than estimated, so check stacked cards.
- **Mid-transition frames.** Snapshot transitions at 3–5 points to confirm they're smooth (for example `--range 4,10 --frames 8`).
- **Nothing cut off** at the edges, and no leftover elements from the previous scene.

Fix issues and re-snapshot before rendering. Rendering takes minutes; a snapshot takes seconds.

## 6. Render and poster

```bash
cd composition && npx hyperframes render -o ../work/render.mp4 -f 30 --quiet
bash <skill>/scripts/bake_poster.sh ../work/render.mp4 <poster-time-seconds> ..
```

`bake_poster.sh` grabs the best frame (usually the title or outro, fully settled) as `poster.jpg`, and overlays it on frame 0. Players and chat apps then show a good thumbnail. Afterwards, confirm the duration with `ffprobe`.
## 7. Iterate on feedback

- **Freeze before you change.** When the user approves a version, copy `video.mp4`, the plan and `composition/` into `vN/` first.
- **Insert a scene mid-video** with `scripts/shift_timeline.py`. It moves every `data-start` and timeline position at or after a time `T` by `+S` seconds. Then add the new section at `[T, T+S)` and update the root and music durations.
- **Keep changes small and targeted.** Change only what the user mentioned, and keep everything they liked.
- Afterwards, grep for removed claims to confirm they're gone everywhere: the video, plan, share copy and any README.

## 8. Handy ffmpeg

```bash
# Uniform slowdown to 1.5x length (video + audio), without re-editing
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=1.5*PTS[v];[0:a]atempo=0.6667[a]" -map "[v]" -map "[a]" out.mp4
# Contact strip of chosen frames from a render (frame number = seconds * fps)
ffmpeg -i video.mp4 -vf "select='eq(n\,120)+eq(n\,900)',scale=640:-1,tile=2x1" -frames:v 1 strip.jpg
# Duration
ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4
```

## 9. Deliver

Tell the user:

- the path to the video, its length, and what changed
- the list of claims to verify (see the honesty rules)
- one specific question to move the next iteration forward

