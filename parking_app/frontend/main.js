const { useState, useEffect } = React;

function ParkingMap() {
  const [spots, setSpots] = useState([]);
  const [weather, setWeather] = useState({});

  useEffect(() => {
    fetch('/api/parking')
      .then(res => res.json())
      .then(data => {
        setSpots(data);
        data.forEach(spot => {
          fetchWeather(spot).then(w => {
            setWeather(prev => ({...prev, [spot.id]: w}));
          });
        });
      });
  }, []);

  useEffect(() => {
    const map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    spots.forEach(spot => {
      const w = weather[spot.id];
      const weatherInfo = w ? `${w.weather[0].description}, ${w.main.temp}\u00B0C` : 'Loading...';
      L.marker([spot.latitude, spot.longitude])
        .addTo(map)
        .bindPopup(`Spot ${spot.id} - ${spot.isAvailable ? 'Available' : 'Occupied'}<br/>${weatherInfo}`);
    });
  }, [spots, weather]);

  return React.createElement('div', {id: 'map'});
}

function fetchWeather(spot) {
  const apiKey = 'YOUR_API_KEY';
  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${spot.latitude}&lon=${spot.longitude}&appid=${apiKey}&units=metric`;
  return fetch(url).then(res => res.json()).catch(() => null);
}

ReactDOM.render(React.createElement(ParkingMap), document.getElementById('root'));
