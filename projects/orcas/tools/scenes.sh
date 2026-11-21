#!/bin/bash
# shot boundaries per source file -> artifacts/scenes/<name>.txt (one cut time per line) + duration
f=$1; b=$(basename "$f"); o=artifacts/scenes/${b%.*}.txt
[ -s "$o" ] && exit 0
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
ffmpeg -v error -i "$f" -vf "scale=320:-2,scdet=threshold=12" -an -f null - 2>&1 | grep -oE 'lavfi.scd.time: [0-9.]+' | awk '{print $2}' > "$o.tmp"
echo "dur $d" > "$o"; cat "$o.tmp" >> "$o"; rm "$o.tmp"
