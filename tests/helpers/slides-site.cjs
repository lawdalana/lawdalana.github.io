const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const { Liquid } = require('liquidjs');
const YAML = require('yaml');
const sass = require('sass');

const root = path.resolve(__dirname, '../..');
const fixtures = {
  empty: [],
  grouped: [
    { category: 'AI / ML', decks: [
      { title: 'First AI deck', url: '/first-slides/' },
      { title: 'Second AI deck', url: '/second-slides/' }
    ] },
    { category: 'Data', decks: [{ title: 'Database deck', url: '/database-slides/' }] }
  ],
  unsafe: [{ category: 'AI <script>alert(1)</script>', decks: [
    { title: '<img src=x onerror=alert(1)>', url: '/safe-slides/' },
    { title: 'JavaScript URL', url: 'javascript:alert(1)' },
    { title: 'Remote URL', url: 'https://evil.invalid/slides/' },
    { title: 'Protocol relative URL', url: '//evil.invalid/slides/' },
    { title: 'Backslash URL', url: '/\\evil.invalid/slides/' }
  ] }]
};

async function catalog() {
  try { return YAML.parse(await fs.readFile(path.join(root, '_data/slides.yml'), 'utf8')) || []; }
  catch (error) { if (error.code === 'ENOENT') return []; throw error; }
}

async function renderHeader(slides, baseurl = '') {
  const liquid = new Liquid({ root: path.join(root, '_includes'), jekyllInclude: true, strictFilters: true });
  liquid.registerFilter('relative_url', input => (baseurl.replace(/\/$/, '') + '/' + String(input).replace(/^\//, '')));
  return liquid.renderFile('Header.html', { site: { baseurl, data: { slides } } });
}

async function startSite() {
  const server = http.createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://localhost');
      const pathname = decodeURIComponent(url.pathname).replace(/^\/garden(?=\/)/, '');
      if (pathname === '/' || pathname === '/notes') {
        const slides = fixtures[url.searchParams.get('fixture')] || await catalog();
        const header = await renderHeader(slides, url.pathname.startsWith('/garden/') ? '/garden' : '');
        response.setHeader('Content-Type', 'text/html; charset=utf-8');
        response.end('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><link rel="stylesheet" href="/assets/css/style.css"><link rel="stylesheet" href="/assets/css/main.css"><link rel="stylesheet" href="/assets/css/Util.css"></head><body>' + header + '<main><h1>Garden</h1><button id="outside">Outside navigation</button></main></body></html>');
        return;
      }
      if (/^\/(first|database|second|safe)-slides\/$/.test(pathname)) {
        response.setHeader('Content-Type', 'text/html; charset=utf-8');
        response.end('<!doctype html><title>Selected deck</title><h1>Selected deck</h1>');
        return;
      }
      const file = path.resolve(root, '.' + pathname, pathname.endsWith('/') ? 'index.html' : '');
      if (!file.startsWith(root + path.sep)) { response.writeHead(403).end(); return; }
      const raw = await fs.readFile(file);
      const ext = path.extname(file);
      response.setHeader('Content-Type', ({ '.css': 'text/css', '.js': 'text/javascript', '.html': 'text/html; charset=utf-8', '.svg': 'image/svg+xml', '.avif': 'image/avif' })[ext] || 'application/octet-stream');
      if (ext === '.css' && raw.toString().startsWith('---')) {
        const source = raw.toString().replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
        response.end(sass.compileString(source, { logger: { warn() {}, debug() {} } }).css);
      } else { response.end(raw); }
    } catch (error) {
      response.writeHead(error.code === 'ENOENT' ? 404 : 500, { 'Content-Type': 'text/plain' });
      response.end(error.message);
    }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  return { server, url: 'http://127.0.0.1:' + server.address().port };
}

module.exports = { root, fixtures, catalog, renderHeader, startSite };
