// Render check for a built DDL activity folder: script errors, phone-width overflow,
// and text spilling outside slides. Needs Playwright (require('playwright')).
// Usage: node check.js <folder> [screenshot-folder]
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.resolve(process.argv[2] || '.');
const shots = process.argv[3] ? path.resolve(process.argv[3]) : null;
(async () => {
  const b = await chromium.launch();
  const errs = [];
  let bad = 0;
  const act = path.join(dir, 'deploy', 'index.html');
  for (const [w, h, name] of [[1280, 800, 'desktop'], [390, 800, 'phone']]) {
    const p = await b.newPage({viewport: {width: w, height: h}});
    p.on('pageerror', e => errs.push('activity: ' + e.message));
    await p.goto('file://' + act); await p.waitForTimeout(600);
    const info = await p.evaluate(() => ({
      sw: document.documentElement.scrollWidth,
      lines: document.querySelectorAll('#conc .row').length,
      cards: document.querySelectorAll('#cards .card').length,
      gaps: document.querySelectorAll('select.gap').length,
      errs: document.querySelectorAll('#errlist .err').length,
    }));
    if (info.sw > w) { bad++; console.log(`OVERFLOW activity ${name}: page is ${info.sw}px wide`); }
    if (name === 'desktop') console.log('activity:', JSON.stringify(info));
    if (shots) await p.screenshot({path: path.join(shots, `activity-${name}.png`), fullPage: true});
  }
  const sl = path.join(dir, 'slides.html');
  if (fs.existsSync(sl)) {
    const html = '<!doctype html><html><head><meta charset="utf-8"></head><body>' + fs.readFileSync(sl, 'utf8') + '</body></html>';
    const tmp = path.join(dir, '.slides-check.html'); fs.writeFileSync(tmp, html);
    const s = await b.newPage({viewport: {width: 1440, height: 810}});
    s.on('pageerror', e => errs.push('slides: ' + e.message));
    await s.goto('file://' + tmp); await s.waitForTimeout(500);
    const n = await s.evaluate(() => document.querySelectorAll('.slide').length);
    for (let i = 1; i <= n; i++) {
      await s.goto('file://' + tmp + '#s' + i); await s.reload(); await s.waitForTimeout(250);
      for (let k = 0; k < 8; k++) { if (!(await s.$('.slide.on .step.hide'))) break; await s.keyboard.press('ArrowRight'); }
      await s.waitForTimeout(300);
      const over = await s.evaluate(() => { const sl = document.querySelector('.slide.on'); const r = sl.getBoundingClientRect(); const out = [];
        sl.querySelectorAll('*').forEach(e => { const q = e.getBoundingClientRect(); if (q.width && (q.right > r.right + 1 || q.bottom > r.bottom + 1)) out.push(e.className || e.tagName); });
        sl.querySelectorAll('.conc').forEach(c => { if (c.scrollWidth > c.clientWidth + 1) out.push('conc (text wider than box)'); });
        return out.slice(0, 5); });
      if (over.length) { bad++; console.log(`OVERFLOW slide ${i}:`, over.join(', ')); }
      if (shots) await s.screenshot({path: path.join(shots, `slide-${String(i).padStart(2, '0')}.png`)});
    }
    console.log('slides:', n);
    fs.unlinkSync(tmp);
  }
  errs.forEach(e => console.log('SCRIPT ERROR', e));
  console.log(errs.length || bad ? 'CHECK FAILED' : 'CHECK OK');
  await b.close();
  process.exit(errs.length || bad ? 1 : 0);
})();
