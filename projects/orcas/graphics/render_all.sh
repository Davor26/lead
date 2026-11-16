#!/usr/bin/env bash
# Render every composition in compositions/ to renders/<name>.mp4 and grab a review frame.
set -u
cd "$(dirname "$0")"
export ONNXRUNTIME_NODE_INSTALL=skip
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
mkdir -p renders review
for f in compositions/${1:-*}.html; do
  n=$(basename "$f" .html)
  [ -s "renders/$n.mp4" ] && [ "renders/$n.mp4" -nt "$f" ] && continue
  cp "$f" index.html
  lint=$(npx -y hyperframes@0.6.70 lint . 2>&1 | grep -E '^\s+[⚠✗]' | grep -v 'compositions/' | head -3)
  if npx -y hyperframes@0.6.70 render . -o "renders/$n.mp4" --quiet >/dev/null 2>&1; then
    d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "renders/$n.mp4")
    ffmpeg -v error -y -ss "$(python3 -c "print(max(0,$d*0.8))")" -i "renders/$n.mp4" -frames:v 1 -vf scale=960:-1 "review/$n.jpg"
    echo "OK   $n ${d}s ${lint}"
  else
    echo "FAIL $n ${lint}"
  fi
done
rm -f index.html
