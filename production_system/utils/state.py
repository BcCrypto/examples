_env = None
_latest_frame = None


def set_env(env):
    global _env
    _env = env


def get_env():
    return _env


def set_latest_frame(frame: bytes):
    global _latest_frame
    _latest_frame = frame


def get_latest_frame():
    return _latest_frame
