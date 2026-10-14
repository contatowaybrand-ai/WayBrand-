// node text.mjs out.png "small" "black" "green" smallFont
import { chromium } from 'playwright'; import path from 'path';
const [out, s, b, g, sf='InterDisplay-Light.otf'] = process.argv.slice(2);
const dir = path.resolve('assets/fonts');
const html = `<style>
@font-face{font-family:S;src:url(assets/fonts/${sf})}
@font-face{font-family:B;src:url(assets/fonts/Bricolage.ttf)}
@font-face{font-family:G;src:url(assets/fonts/Anton-Regular.ttf)}
html,body{margin:0;background:transparent}
div{position:absolute;left:72px;white-space:pre;line-height:1}
#s{font:41px S;letter-spacing:-1px;color:rgb(20,24,26);top:${process.env.SY||0}px}
#b{font:124px B;font-variation-settings:'wght' 800,'opsz' 96,'wdth' 100;letter-spacing:-5px;color:rgb(12,23,24);top:${process.env.BY||200}px}
#g{font:130px G;letter-spacing:-0.5px;color:rgb(0,179,144);top:${process.env.GY||450}px}
</style><div id=s>${s}</div><div id=b>${b}</div><div id=g>${g}</div>`;
const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1080, height: 1350 } });
const fs = await import('fs'); fs.writeFileSync(dir + '/../_t.html', html); await p.goto('file://' + dir + '/../_t.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
const pos = {}; for (const id of ['s','b','g']) pos[id] = await p.$eval('#'+id, e => e.textContent);
await p.screenshot({ path: out, omitBackground: true }); await br.close();
