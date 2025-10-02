# Mixins to demonstrate multiple inheritance.

class LoggingMixin:
    # Adds a simple log() helper to any class.
    def log(self, message: str):
        print(f"[LOG] {self.__class__.__name__}: {message}")

class ErrorHandlingMixin:
    # Wraps a callable to catch and re-raise while logging.
    def safe_run(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] {self.__class__.__name__}: {e}")
            raise

