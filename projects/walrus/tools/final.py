"""Final: chapter chunks -> one H.264 video stream, muxed WITH the final audio mix; verify streams and duration."""
import json, subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]
OUT = P.parents[1]/'output/walrus/why_polar_bears_throw_rocks_at_walruses.mp4'
TL = json.load(open(P/'artifacts/timeline.json'))
subprocess.run([sys.executable, str(P/'tools/build.py'), 'chunks'], check=True)
video = P/'renders/video_only.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(P/'renders/chunks/all.txt'), '-c', 'copy', str(video)], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(video), '-i', str(P/'assets/audio/final_mix.wav'),
                '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                '-shortest', '-movflags', '+faststart',
                '-metadata', "title=Why Polar Bears Throw Rocks at Walruses", '-metadata', 'artist=Naturexplore', str(OUT)], check=True)
pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(OUT)], capture_output=True, text=True).stdout)
v = [s for s in pr['streams'] if s['codec_type'] == 'video']; a = [s for s in pr['streams'] if s['codec_type'] == 'audio']
print('video:', v[0]['codec_name'], f"{v[0]['width']}x{v[0]['height']}", v[0]['r_frame_rate'], v[0].get('nb_frames'))
print('audio:', a[0]['codec_name'] if a else 'MISSING', a[0].get('sample_rate') if a else '', a[0].get('channels') if a else '')
print('duration:', pr['format']['duration'], 'expected', TL['total'], 'size MB', round(int(pr['format']['size']) / 1e6))
assert a, 'no audio stream!'
