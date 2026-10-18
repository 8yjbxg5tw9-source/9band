#!/usr/bin/env node
/**
 * Export the existing two P-01 lessons, not a new/validated lesson batch.
 * All source content stays unchanged. SVGs are embedded as vector images;
 * formerly collapsible scripts and answer keys are expanded for paper.
 *
 * Optional dependencies (outside the core standard-library QA toolchain):
 * npm install --prefix .cache/pdf-tools --no-audit --no-fund \
 *   @sparticuz/chromium@153.0.0 puppeteer-core@25.14.0 markdown-it@15.0.3
 * node scripts/export_pilot_pdf.cjs
 */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const {createRequire} = require('node:module');

const ROOT = path.resolve(__dirname, '..');
const OUTPUT = path.join(ROOT, 'exports');
const CACHE = path.join(ROOT, '.cache', 'pdf-export');
const deps = createRequire(path.join(ROOT, '.cache', 'pdf-tools', 'package.json'));
const IDS = ['A0-M1-U1-L01', 'A0-M1-U1-L02'];
const ICONS = new Set(['see.svg', 'say.svg', 'write.svg', 'select.svg', 'recall.svg', 'ear.svg']);
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const escape = s => s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

const CSS = `
@page { size: A4; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'DejaVu Sans', sans-serif; color: #203846; margin: 0;
       font-size: 12.3pt; line-height: 1.48; background: white; }
article + article { break-before: page; }
h1 { color: #0f766e; font-size: 24pt; font-weight: 700; line-height: 1.2;
     margin: 0 0 5mm; padding: 0 0 4mm; border-bottom: 2px solid #0f766e; }
blockquote { margin: 0 0 7mm; color: #536d75; font-size: 10pt; }
blockquote p { margin: 0; }
h2 { color: #0f766e; font-size: 16pt; line-height: 1.25; margin: 8mm 0 3.5mm;
     border-top: 1px solid #dce7e3; padding-top: 4mm; break-after: avoid; }
/* Section 21 contains only the source machine record, not learner work. */
h2[data-section="21"] { display: none; }
h3 { font-size: 13.7pt; margin: 5mm 0 3mm; color: #203846; break-after: avoid; }
p { margin: 2.7mm 0; orphans: 3; widows: 3; }
strong { font-weight: 700; }
img { max-width: 100%; object-fit: contain; }
img.icon { width: 8mm; height: 8mm; vertical-align: middle; margin: 0 1mm; }
h2 img.icon { width: 8mm; height: 8mm; }
img.figure { width: 147mm; height: auto; max-height: 167mm; vertical-align: middle; }
p.figure-block { text-align: center; margin: 4mm 0; break-inside: avoid; }
p.inline-figure { break-inside: avoid; }
p.inline-figure img.figure { width: 90mm; max-height: 75mm; }
p.scene-reference { display: inline-block; width: 48%; text-align: center;
                    vertical-align: top; margin: 3mm 0; break-inside: avoid; }
p.scene-reference img.figure { display: block; width: 100%; max-height: 44mm; }
table { border-collapse: collapse; width: 100%; margin: 3.5mm 0 5mm;
        table-layout: fixed; font-size: 11.4pt; line-height: 1.44; }
thead { display: table-header-group; }
tfoot { display: table-footer-group; }
tr { break-inside: avoid; page-break-inside: avoid; }
th, td { border: 1px solid #cddcd7; padding: 2.8mm 2.5mm; vertical-align: middle;
         overflow-wrap: anywhere; }
th { background: #eaf3ef; color: #0f766e; font-weight: 700; text-align: left; }
tbody tr:nth-child(even) { background: #fbfcf9; }
td img.figure { display: block; width: 100%; max-height: 53mm; margin: 1mm auto; }
table.tasks col:first-child { width: 11%; }
table.tasks col:nth-child(2) { width: 56%; }
table.tasks col:nth-child(3) { width: 33%; }
table.examples col:first-child { width: 11%; }
table.examples col:nth-child(2) { width: 51%; }
table.examples col:nth-child(3) { width: 38%; }
table.speaking col:first-child { width: 11%; }
table.speaking col:nth-child(2) { width: 40%; }
table.speaking col:nth-child(3) { width: 49%; }
table.contrast col:first-child { width: 49%; }
table.contrast col:nth-child(2), table.contrast col:nth-child(3) { width: 25.5%; }
table.keys td, table.keys th { padding: 1.65mm 2.5mm; }
table.review td, table.review th { padding: 1.5mm 2.5mm; }
p.figure-block[data-section="19"] img.figure { width: 120mm; }
ul[data-section="20"] li { margin: 1.3mm 0; }
table.keys col:first-child { width: 13%; }
table.keys col:nth-child(2) { width: 87%; }
table.goals col:first-child { width: 78%; }
table.goals col:nth-child(2) { width: 22%; }
table.goals td img.figure { max-height: 54mm; width: 110mm; }
.disclosure { margin: 5mm 0; padding: 4mm; border: 1px solid #b7cdc5;
              background: #f7faf7; border-radius: 2mm; }
.disclosure.script { break-inside: avoid; }
.disclosure.key { background: white; padding: 0; border: 0; }
.disclosure-label { font-size: 10pt; color: #0f766e; font-weight: bold; margin-bottom: 3mm; }
ol { padding-left: 10mm; }
li { margin: 2.5mm 0; break-inside: avoid; }
ul { padding-left: 7mm; }
input[type=checkbox] { appearance: none; width: 4mm; height: 4mm; border: 1px solid #536d75;
                       vertical-align: middle; margin: 0 2mm 0 0; }
`;

function lessonHtml(id, md, evidence) {
  const source = path.join(ROOT, 'content', 'A0', `${id}.md`);
  let text = fs.readFileSync(source, 'utf8');
  evidence.inputs[path.relative(ROOT, source)] = hash(Buffer.from(text));
  // Machine records remain hidden, exactly as in the source Markdown view.
  text = text.replace(/<!--[\s\S]*?-->/g, '');
  // Explicitly expand each disclosure; never let a printer omit a key/script.
  text = text.replace(/<details>\s*<summary>([\s\S]*?)<\/summary>/g, (_, label) => {
    const kind = label.includes('SCRIPT ONLY') ? 'script' : 'key';
    return `\n\n<div class="disclosure ${kind}">\n<div class="disclosure-label">${label}</div>\n\n`;
  }).replace(/<\/details>/g, '\n\n</div>\n\n');
  // Printable empty checkboxes, not literal Markdown task-list syntax.
  text = text.replace(/^- \[ \] /gm, '- <input type="checkbox" disabled aria-label="Unchecked"/> ');
  const original = md.renderer.rules.image;
  md.renderer.rules.image = (tokens, index, options, env, renderer) => {
    const token = tokens[index];
    const relative = token.attrGet('src');
    const asset = path.resolve(path.dirname(source), relative);
    if (!asset.startsWith(path.join(ROOT, 'content', 'A0', 'assets') + path.sep) || !fs.existsSync(asset)) {
      throw new Error(`Missing/unsafe image: ${relative}`);
    }
    const bytes = fs.readFileSync(asset);
    const name = path.basename(asset);
    token.attrSet('src', `data:image/svg+xml;base64,${bytes.toString('base64')}`);
    token.attrSet('class', ICONS.has(name) ? 'icon' : 'figure');
    token.attrSet('data-asset', name);
    evidence.inputs[path.relative(ROOT, asset)] = hash(bytes);
    return original(tokens, index, options, env, renderer);
  };
  const html = md.render(text);
  md.renderer.rules.image = original;
  return `<article data-lesson="${id}">${html}</article>`;
}

async function preparePage(page, html) {
  // All pictures and text are local/data URIs. No web font/image dependency.
  await page.setRequestInterception(true);
  page.on('request', req => /^(data:|about:)/.test(req.url()) ? req.continue() : req.abort());
  await page.setContent(html, {waitUntil:'load'});
  await page.emulateMediaType('print');
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all(Array.from(document.images, img => img.decode()));
    for (const article of document.querySelectorAll('article')) {
      let section = 0;
      for (const node of article.children) {
        if (node.tagName === 'H2') section = Number.parseInt(node.textContent, 10);
        node.dataset.section = String(section);
        if (section === 19 && node.tagName === 'TABLE') node.classList.add('review');
      }
    }
    for (const p of document.querySelectorAll('p')) {
      if (!p.querySelector('img.figure')) continue;
      const label = p.textContent.trim();
      p.classList.add(/^P[12]:$/.test(label) ? 'scene-reference' : label ? 'inline-figure' : 'figure-block');
    }
    for (const table of document.querySelectorAll('table')) {
      const row = table.querySelector('tbody tr');
      const cells = row ? Array.from(row.cells) : [];
      const first = cells[0]?.textContent.trim() || '';
      let name;
      if (cells.length === 2 && /^[HLRABSTWQ]\d{2}$/.test(first)) name = 'keys';
      else if (cells.length === 3 && /^S\d{2}$/.test(first)) name = 'speaking';
      else if (cells.length === 3 && /^E\d{2}$/.test(first)) name = 'examples';
      else if (cells.length === 3 && /^[HLRABTWQ]\d{2}$/.test(first)) name = 'tasks';
      else if (cells.length === 3 && /✗/.test(table.querySelector('thead')?.textContent || '')) name = 'contrast';
      else if (cells.length === 2 && table.querySelector('img.figure')) name = 'goals';
      if (name) {
        table.classList.add(name);
        const cols = document.createElement('colgroup');
        cells.forEach(() => cols.append(document.createElement('col')));
        table.prepend(cols);
      }
    }
  });
  return page.evaluate(() => ({
    lessons: Array.from(document.querySelectorAll('article')).map(article => ({
      id:article.dataset.lesson,
      numberedSections:article.querySelectorAll('h2').length,
      scriptsExpanded:article.querySelectorAll('.disclosure.script').length,
      scriptLines:article.querySelectorAll('.disclosure.script ol li').length,
      keysExpanded:article.querySelectorAll('.disclosure.key').length,
      answerRows:article.querySelectorAll('table.keys tbody tr').length,
      imageInstances:article.querySelectorAll('img').length,
    })),
    missingImages:Array.from(document.images).filter(img => !img.complete || !img.naturalWidth).map(img => img.dataset.asset),
    horizontalOverflows:Array.from(document.querySelectorAll('table,p,h1,h2,h3'))
      .filter(node => node.getBoundingClientRect().right > document.documentElement.clientWidth+1).length,
  }));
}

(async () => {
  fs.mkdirSync(OUTPUT, {recursive:true});
  fs.mkdirSync(CACHE, {recursive:true});
  const mod = await import(deps.resolve('@sparticuz/chromium'));
  const chromium = mod.default;
  const bin = path.join(path.dirname(deps.resolve('@sparticuz/chromium')), '..', 'bin');
  // Minimal Debian sandboxes may lack NSS/NSPR. Use the bundled local libs;
  // this does not download a browser or any libraries from a separate host.
  for (const archive of ['al2023.tar.br','fonts.tar.br']) await mod.inflate(path.join(bin, archive));
  mod.setupLambdaEnvironment(path.join(os.tmpdir(), 'al2023', 'lib'));
  for (const name of ['DejaVuSans.ttf', 'DejaVuSans-Bold.ttf']) {
    const source = path.join('/usr/share/fonts/truetype/dejavu', name);
    if (!fs.existsSync(source)) throw new Error(`Required Unicode font missing: ${source}`);
    fs.copyFileSync(source, path.join(os.tmpdir(), 'fonts', name));
  }
  const puppeteer = deps('puppeteer-core');
  const md = deps('markdown-it')({html:true, typographer:false, breaks:false});
  const evidence = {status:'exported; PDF inspection still required', scope:'P-01 existing drafts only', inputs:{}, outputs:[]};
  const fragments = Object.fromEntries(IDS.map(id => [id, lessonHtml(id, md, evidence)]));
  const browser = await puppeteer.launch({executablePath:await chromium.executablePath(), args:chromium.args, headless:true});
  try {
    evidence.renderer = await browser.version();
    const jobs = [
      {name:'P-01-Lessons-1-and-2.pdf', ids:IDS},
      ...IDS.map(id => ({name:`${id}.pdf`, ids:[id]})),
    ];
    for (const job of jobs) {
      const page = await browser.newPage();
      try {
        await page.setViewport({width:680,height:1000,deviceScaleFactor:1});
        const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${escape(job.ids.join(' + '))} — Draft</title><style>${CSS}</style></head><body>${job.ids.map(id => fragments[id]).join('\n')}</body></html>`;
        fs.writeFileSync(path.join(CACHE, job.name.replace('.pdf','.html')), html);
        const checks = await preparePage(page, html);
        if (checks.missingImages.length || checks.horizontalOverflows) throw new Error(`Layout/resource failure: ${JSON.stringify(checks)}`);
        for (const lesson of checks.lessons) {
          const expected = lesson.id.endsWith('01') ? 39 : 47;
          if (lesson.numberedSections !== 21 || lesson.scriptsExpanded !== 1 || lesson.scriptLines !== 4 || lesson.keysExpanded !== 1 || lesson.answerRows !== expected) {
            throw new Error(`Missing content in export: ${JSON.stringify(lesson)}`);
          }
        }
        const output = path.join(OUTPUT, job.name);
        await page.pdf({path:output, format:'A4', printBackground:true, preferCSSPageSize:true,
          margin:{top:'14mm',right:'14mm',bottom:'17mm',left:'14mm'},
          displayHeaderFooter:true, headerTemplate:'<div></div>',
          footerTemplate:'<div style="font-family:DejaVu Sans,sans-serif;font-size:8px;color:#6b7d80;width:100%;margin:0 14mm;display:flex;justify-content:space-between"><span>P-01 · DRAFT</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
          tagged:true, outline:true,
        });
        evidence.outputs.push({path:path.relative(ROOT,output),sha256:hash(fs.readFileSync(output)),...checks});
        console.log(`Exported ${job.name}: all sections, ${checks.lessons.reduce((n,l)=>n+l.answerRows,0)} answer rows, no missing images.`);
      } finally { await page.close(); }
    }
  } finally { await browser.close(); }
  evidence.inputs['scripts/export_pilot_pdf.cjs'] = hash(fs.readFileSync(__filename));
  fs.writeFileSync(path.join(CACHE,'export-evidence.json'),JSON.stringify(evidence,null,2)+'\n');
})().catch(error => {console.error(error); process.exitCode=1;});
