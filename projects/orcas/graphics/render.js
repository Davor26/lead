// usage: node render.js jobs.json   (jobs: [{name, dur, out, params, still}])
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(__dirname, 'index.html'));
  await page.evaluate(() => document.fonts.ready);
  for (const j of jobs) {
    const fps = 30, n = j.still ? 1 : Math.round(j.dur * fps);
    const alpha = await page.evaluate(([nm, D, p]) => R(nm, 0, D, p), [j.name, j.dur, j.params]);
    const t0 = Date.now();
    if (j.still) {
      await page.evaluate(([nm, t, D, p]) => R(nm, t, D, p), [j.name, j.at || 2.0, j.dur, j.params]);
      await page.screenshot({ path: j.out, omitBackground: true });
      console.log('still', j.out); continue;
    }
    const args = alpha
      ? ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'png', '-i', '-', '-c:v', 'qtrle', '-pix_fmt', 'argb', j.out]
      : ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', j.out];
    const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < n; f++) {
      await page.evaluate(([nm, t, D, p]) => R(nm, t, D, p), [j.name, f / fps, j.dur, j.params]);
      const buf = await page.screenshot(alpha ? { type: 'png', omitBackground: true } : { type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log(j.out, n, 'frames', ((Date.now() - t0) / 1000).toFixed(1) + 's');
  }
  await browser.close();
})();
