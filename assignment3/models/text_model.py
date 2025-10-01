# Concrete handler for text classification (sentiment).

from transformers import pipeline
from assignment3.models.base import ModelHandlerBase

class TextModelHandler(ModelHandlerBase):
    def _build_pipeline(self):
        # Build a Transformers pipeline for text classification.
        return pipeline("text-classification", model=self.model_id)

    def _format_output(self, raw_output):
        # raw_output is a list of dicts; display top prediction.
        if not raw_output:
            return "No result."
        best = raw_output[0]
        label = best.get("label", "?")
        score = best.get("score", 0.0)
        return f"Sentiment: {label} (confidence {score:.2f})"
