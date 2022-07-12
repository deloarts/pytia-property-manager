"""
    Module that holds decorators for the app.
"""

import functools
import time

from pytia.log import log


def timer(func):
    """Print the runtime of the decorated function."""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        log.debug(
            f"Function {func.__name__!r} took {(end_time-start_time):.4f}s to complete."
        )
        return value

    return wrapper_timer
