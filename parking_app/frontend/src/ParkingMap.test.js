const {JSDOM} = require('jsdom');
const fs = require('fs');
const path = require('path');

test('loads parking map page', () => {
  const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');
  const dom = new JSDOM(html, { runScripts: 'outside-only' });
  expect(dom.window.document.getElementById('root')).not.toBeNull();
});
