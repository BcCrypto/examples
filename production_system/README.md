# Production System Example

This example reorganizes a complex training and API stack into a small package.

## Components

- **FastAPI** service exposing webhook, metric, and dashboard endpoints.
- **Prometheus** gauges to track portfolio metrics.
- **LangGraph** and **AutoGen** agents used for signal analysis.
- **Gym** environment and **stable-baselines3** PPO agent training in an infinite loop.

## Running

```bash
python -m production_system.main
```

The script starts the API on `localhost:8000`, exposes metrics on `8001`, and
trains the reinforcement learning model, saving checkpoints periodically.

Open `http://localhost:8000/dashboard` to view real-time metrics and the latest
rendered frame from the training environment.
