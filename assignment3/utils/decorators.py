# Reusable decorators for logging and timing.

import time
import functools

def log_call(func):
    # Logs the class and function name with basic args info.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0].__class__.__name__ if args else "<fn>"
        print(f"[LOG] {cls}.{func.__name__} args={args[1:]}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

def timeit(func):
    # Measures execution time in milliseconds.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            ms = (time.time() - start) * 1000.0
            print(f"[TIME] {func.__name__} took {ms:.1f} ms")
    return wrapper
