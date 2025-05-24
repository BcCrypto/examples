# Parking App Example

This example demonstrates a simple parking spot map with weather forecasts.

## Backend

The backend provides parking spot data on `/api/parking` using Node's built-in `http` module.
Run it with:

```bash
node backend/server.js
```

## Frontend

The frontend is a small React app served from static files. Open `frontend/index.html` in a browser.
It fetches parking spots from the backend and displays them on a Leaflet map along with weather information from OpenWeatherMap.

## Tests

Unit tests use Jest. Run them with:

```bash
npm test --prefix frontend
```

Note that installing dependencies may require network access.
