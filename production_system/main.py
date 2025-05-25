import asyncio
from threading import Thread

import uvicorn

from .api.server import app, start_metrics_server
from .agents import build_lang_app, create_agents
from .rl.environment import create_model, train_forever
from .utils.state import set_env


async def run_training():
    model, env = create_model()
    set_env(env)
    train_forever(model, env)


def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main():
    _ = build_lang_app()
    signal_agent, decision_agent, user_agent = create_agents()
    user_agent.initiate_chat(signal_agent, message="Analyze signal trend.")
    user_agent.initiate_chat(decision_agent, message="Decide based on signal.")

    Thread(target=start_api).start()
    start_metrics_server()
    asyncio.run(run_training())


if __name__ == "__main__":
    main()
