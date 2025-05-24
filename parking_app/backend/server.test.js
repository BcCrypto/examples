const http = require('http');
const { start } = require('./server');

test('GET /api/parking returns list', done => {
  const srv = start(0);
  const { port } = srv.address();
  http.get(`http://localhost:${port}/api/parking`, res => {
    expect(res.statusCode).toBe(200);
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
      const spots = JSON.parse(data);
      expect(Array.isArray(spots)).toBe(true);
      srv.close();
      done();
    });
  });
});
