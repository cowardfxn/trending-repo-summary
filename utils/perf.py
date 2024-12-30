from functools import wraps
from time import time


def timer(func):
    """
    Timer decorator
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"[{func.__name__}] time elapsed: {end - start:.2f} seconds")
        return result

    return wrapper


def atimer(func):
    """
    Timer decorator for async functions
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()
        result = await func(*args, **kwargs)
        end = time()
        print(f"[{func.__name__}] time elapsed: {end - start:.2f} seconds")
        return result

    return wrapper
