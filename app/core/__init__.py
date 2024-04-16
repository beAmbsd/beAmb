import os


def get_virt_env():
    """Simple retrieval function.
    Returns lowercase USER or raises OSError."""
    virt_env = os.getenv("TEST_ENV")

    if virt_env is None:
        raise OSError("USER environment is not set.")

    return virt_env.lower()