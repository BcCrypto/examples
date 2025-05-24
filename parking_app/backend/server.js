const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

const parkingSpots = [
  { id: 1, latitude: 51.505, longitude: -0.09, isAvailable: true, price: 2.5 },
  { id: 2, latitude: 51.515, longitude: -0.1, isAvailable: false, price: 3.0 }
];

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  if (parsedUrl.pathname === '/api/parking') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(parkingSpots));
    return;
  }

  let filePath = 'index.html';
  if (parsedUrl.pathname === '/main.js') {
    filePath = 'main.js';
  }

  const fullPath = path.join(__dirname, '../frontend', filePath);
  fs.readFile(fullPath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end();
      return;
    }
    const ext = path.extname(fullPath);
    const type = ext === '.js' ? 'application/javascript' : 'text/html';
    res.writeHead(200, { 'Content-Type': type });
    res.end(data);
  });
});

function start(port = 3000) {
  return server.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
}

if (require.main === module) {
  start();
}

module.exports = { start };
