from transformers import pipeline
import time

# This decorator measures how long the function takes to run
def time_logger(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()  # Record start time
        result = func(*args, **kwargs)  # Execute the function
        print(f"[text time] {func.__name__} took {time.time()-t0:.3f}s")  # Print elapsed time
        return result  # Return the result
    return wrapper

# This decorator prints the prediction result for debugging
def result_logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # Execute the function
        print(f"[text result] {result}")  # Print the result
        return result  # Return the result
    return wrapper

class ModelBase:
    """Defines a common interface for all models (polymorphism)."""
    def predict(self, input_data):
        raise NotImplementedError  # Must be implemented by subclasses

class TextModel(ModelBase):
    # A wrapper for Hugging Face Text Classification models.
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self._model_name = model_name  # Store model name
        try:
            # Initialize Hugging Face pipeline for text classification
            self._pipe = pipeline("text-classification", model=self._model_name)
            print(f"Loaded text pipeline: {self._model_name}")
        except Exception:
            # Handle initialization failure
            print("Warning: Could not initialize text pipeline.")
            self._pipe = None

    @time_logger     # First decorator → logs how long prediction took
    @result_logger   # Second decorator → logs the prediction result
    def predict(self, text: str):
        """
        Run text classification (sentiment analysis) on the input text.

        Parameters:
            text (str): Input string to analyze.

        Returns:
            List of (label, score) tuples (e.g., [("POSITIVE", 0.998)]).
        """
        if self._pipe is None:
            # Raise error if pipeline is not initialized
            raise RuntimeError("Text pipeline not initialized.")
           
        # Run the Hugging Face text classification model
        res = self._pipe(text)
        # Extract label and score from each result
        return [(prediction["label"], float(prediction["score"])) for prediction in res]
