import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const R = '/home/user/Baumpflege-Webseite/brand/logo';
const jobs = JSON.parse(fs.readFileSync('brand_jobs.json', 'utf8'));
const b = await chromium.launch();
const p = await b.newPage();
for (const j of jobs) {
  const svg = fs.readFileSync(R + '/svg/' + j.name + '.svg', 'utf8');
  if (j.kind === 'png') {
    const W = j.name.includes('symbol') ? 1000 : 2000;
    const H = Math.round(W * j.h / j.w);
    await p.setViewportSize({ width: W, height: H });
    await p.setContent('<html><body style="margin:0;background:transparent">' + svg.replace(/width="[^"]*" height="[^"]*"/, 'width="' + W + '" height="' + H + '"') + '</body></html>');
    await p.locator('svg').screenshot({ path: R + '/png/' + j.name + '.png', omitBackground: true });
  } else {
    const Wmm = j.name.includes('symbol') ? 60 : 200;
    const Hmm = Wmm * j.h / j.w;
    await p.setContent('<html><head><style>@page{size:' + Wmm + 'mm ' + Hmm.toFixed(2) + 'mm;margin:0}html,body{margin:0}svg{display:block;width:' + Wmm + 'mm;height:' + Hmm.toFixed(2) + 'mm}</style></head><body>' + svg + '</body></html>');
    await p.pdf({ path: R + '/pdf/' + j.name + '.pdf', width: Wmm + 'mm', height: Hmm.toFixed(2) + 'mm', printBackground: false, pageRanges: '1' });
  }
}
await b.close();
console.log('ok', jobs.length);
