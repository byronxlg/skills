#!/usr/bin/env bash
# Pick a poster frame and bake it in as frame 0, so players and chat apps show a good thumbnail.
# Usage: bake_poster.sh <render.mp4> <poster-time-seconds> <out-dir>
# Writes <out-dir>/poster.jpg and <out-dir>/video.mp4.
set -euo pipefail
in="$1"; t="$2"; out="${3:-.}"
ffmpeg -y -loglevel error -ss "$t" -i "$in" -frames:v 1 -q:v 2 "$out/poster.jpg"
ffmpeg -y -loglevel error -i "$in" -i "$out/poster.jpg" \
  -filter_complex "[0:v][1:v]overlay=enable='eq(n,0)'" \
  -c:a copy -movflags +faststart "$out/video.mp4"
echo "poster: $out/poster.jpg"
echo "video:  $out/video.mp4 ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out/video.mp4")s)"
