const React = require('react');
const { render, screen } = require('@testing-library/react');
const { ParkingMap, fetchWeather } = require('../main');

beforeEach(() => {
  global.fetch = jest.fn(() => Promise.resolve({
    json: () => Promise.resolve({ weather: [{ description: 'clear' }], main: { temp: 20 } })
  }));
});

test('fetchWeather returns weather info', async () => {
  const data = await fetchWeather({ latitude: 0, longitude: 0 });
  expect(data.main.temp).toBe(20);
});

test('renders map container', () => {
  const { container } = render(React.createElement(ParkingMap));
  expect(container.querySelector('#map')).toBeInTheDocument();
});
