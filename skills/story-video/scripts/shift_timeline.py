#!/usr/bin/env python3
"""Make room for a new scene: shift everything at or after T seconds by +S seconds.

Usage: python3 shift_timeline.py composition/index.html T S

Moves every data-start >= T (sections and audio), and every decimal timeline
position >= T inside the <script> block (numbers like 41.05 passed to tl.*).
Afterwards, add the new section at [T, T+S), then update the root data-duration,
the music duration and its volume automation by hand. Back up the file first.
"""
import re
import sys

path, T, S = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
src = open(path).read()


def fmt(v):
    return f"{v:g}"


def shift_attr(m):
    v = float(m.group(1))
    return f'data-start="{fmt(v + S) if v >= T else m.group(1)}"'


src = re.sub(r'data-start="([\d.]+)"', shift_attr, src)

a = src.rindex("<script>")
b = src.index("</script>", a)
js = src[a:b]
# Only decimal literals: timeline positions are written with a decimal point (e.g. 35.05),
# which avoids touching integers like pixel sizes, indices or durations such as 0.3 below T.
js = re.sub(r"(?<![\w.#-])\d+\.\d+(?!\w)", lambda m: fmt(float(m.group(0)) + S) if float(m.group(0)) >= T else m.group(0), js)
src = src[:a] + js + src[b:]

open(path, "w").write(src)
print(f"Shifted everything at or after {fmt(T)}s by +{fmt(S)}s. Now update root/music durations and add the new scene.")
