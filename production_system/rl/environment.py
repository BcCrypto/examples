import numpy as np
import gym
from gym import spaces
from stable_baselines3 import PPO


class InfiniteRenderEnv(gym.Env):
    """Simple environment generating random 64x64 RGB observations."""

    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=1, shape=(64, 64, 3), dtype=np.float32)
        self.action_space = spaces.Discrete(5)
        self.iteration = 0

    def reset(self):
        self.iteration = 0
        return np.random.rand(64, 64, 3).astype(np.float32)

    def step(self, action):
        self.iteration += 1
        obs = np.clip(np.random.rand(64, 64, 3) + action * 0.1, 0, 1).astype(np.float32)
        reward = float(action) / 5.0
        done = self.iteration > 1000
        return obs, reward, done, {}

    def render(self, mode="human"):
        pass


def create_model():
    """Return PPO model for the environment."""
    env = InfiniteRenderEnv()
    model = PPO("CnnPolicy", env, verbose=1)
    return model, env


def train_forever(model, env, save_interval=10000):
    """Train model indefinitely saving checkpoints."""
    import time

    while True:
        model.learn(total_timesteps=save_interval)
        model.save(f"ray_model_checkpoint_{int(time.time())}")
        print("Checkpoint saved. Continuing training...")
