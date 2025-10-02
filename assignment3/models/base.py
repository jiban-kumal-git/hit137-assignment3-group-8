# Abstract base class for model handlers.
# Encapsulation via private attributes; polymorphic process(); decorators attached.

from abc import ABC, abstractmethod
from assignment3.utils.decorators import log_call, timeit
from assignment3.utils.mixins import LoggingMixin, ErrorHandlingMixin

class ModelHandlerBase(ABC, LoggingMixin, ErrorHandlingMixin):
    def __init__(self, model_id: str):
        # Private attributes (encapsulation).
        self.__model_id = model_id
        self.__pipeline = None  # lazy init

    @property
    def model_id(self) -> str:
        # Expose model id read-only.
        return self.__model_id

    def _get_pipeline(self):
        # Lazily build and cache the pipeline instance.
        if self.__pipeline is None:
            self.__pipeline = self._build_pipeline()
        return self.__pipeline

    @abstractmethod
    def _build_pipeline(self):
        # Subclasses construct and return the underlying pipeline.
        ...

    @abstractmethod
    def _format_output(self, raw_output):
        # Subclasses convert raw outputs to a display string.
        ...

    @log_call
    @timeit
    def process(self, input_data):
        # Default process flow; can be overridden by subclasses.
        pipe = self._get_pipeline()
        raw = pipe(input_data)
        return self._format_output(raw)
