import io
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import PPO


class InfiniteRenderEnv(gym.Env):
    """Simple environment generating random 64x64 RGB observations."""

    def __init__(self):
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(64, 64, 3), dtype=np.float32
        )
        self.action_space = spaces.Discrete(5)
        self.iteration = 0
        self.current_obs = np.zeros((64, 64, 3), dtype=np.float32)

    def reset(self):
        self.iteration = 0
        self.current_obs = np.random.rand(64, 64, 3).astype(np.float32)
        return self.current_obs

    def step(self, action):
        self.iteration += 1
        obs = np.clip(
            np.random.rand(64, 64, 3) + action * 0.1, 0, 1
        ).astype(np.float32)
        self.current_obs = obs
        reward = float(action) / 5.0
        done = self.iteration > 1000
        return obs, reward, done, {}

    def render(self, mode="human"):
        if mode == "png":
            return self._to_png_bytes(self.current_obs)
        if mode == "rgb_array":
            return (self.current_obs * 255).astype(np.uint8)
        return None

    @staticmethod
    def _to_png_bytes(arr: np.ndarray) -> bytes:
        """Encode an RGB image to PNG using only the standard library."""
        import struct
        import zlib

        h, w, _ = arr.shape
        arr8 = (arr * 255).astype(np.uint8)
        raw = b"".join(b"\x00" + arr8[i].tobytes() for i in range(h))
        compressor = zlib.compressobj()
        data = compressor.compress(raw) + compressor.flush()

        def chunk(chunk_type: bytes, data: bytes) -> bytes:
            return (
                struct.pack(">I", len(data))
                + chunk_type
                + data
                + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
            )

        png = b"\x89PNG\r\n\x1a\n"
        ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
        png += chunk(b"IHDR", ihdr)
        png += chunk(b"IDAT", data)
        png += chunk(b"IEND", b"")
        return png


def create_model():
    """Return PPO model for the environment."""
    env = InfiniteRenderEnv()
    model = PPO("CnnPolicy", env, verbose=1)
    return model, env


def train_forever(model, env, save_interval=10000):
    """Train model indefinitely saving checkpoints."""
    import time
    from ..utils.metrics import set_token_estimate
    from ..utils.state import set_latest_frame

    while True:
        model.learn(total_timesteps=save_interval)
        model.save(f"ray_model_checkpoint_{int(time.time())}")
        set_token_estimate(env.iteration)
        set_latest_frame(env.render("png"))
        print("Checkpoint saved. Continuing training...")
