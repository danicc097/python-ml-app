import timeit
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from loguru import logger


def func_timer(method: Callable):  # type: ignore
    """
    Log execution time of a function.
    """

    @wraps(method)
    def __func_timer(*args, **kwargs):

        start_time = timeit.default_timer()
        result = method(*args, **kwargs)
        elapsed = round(timeit.default_timer() - start_time, 4)

        logger.info(f"Timing method={method.__code__}; seconds={elapsed}.")

        return result

    return __func_timer
