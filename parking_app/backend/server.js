const http = require('http');
const url = require('url');

const parkingSpots = [
  { id: 1, latitude: 51.505, longitude: -0.09, isAvailable: true, price: 2.5 },
  { id: 2, latitude: 51.515, longitude: -0.1, isAvailable: false, price: 3.0 }
];

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  if (parsedUrl.pathname === '/api/parking') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(parkingSpots));
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
});
