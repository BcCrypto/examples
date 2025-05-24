# Parking App Example

This example demonstrates a simple parking spot map with weather forecasts.

## Backend

The backend provides parking spot data on `/api/parking` and also serves the static frontend files.
Run it with:

```bash
node backend/server.js
```

## Frontend

The frontend is a small React app. Once the server is running, open `http://localhost:3000` in a browser.
It fetches parking spots from the backend and displays them on a Leaflet map along with weather information from OpenWeatherMap. Set the `OPEN_WEATHER_KEY` environment variable or define `window.OPEN_WEATHER_KEY` before loading the page to retrieve weather data.

## Tests

Unit tests use Jest. Install dependencies and run them with:

```bash
npm install --prefix frontend && npm test --prefix frontend
```

The backend tests can be run similarly:

```bash
npm install --prefix backend && npm test --prefix backend
```

Note that installing dependencies may require network access.
