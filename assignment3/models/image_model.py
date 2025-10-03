# assignment3/models/image_model.py
# Image classification handler using Hugging Face ViT.
# Shows top-3 labels with confidence scores.

from typing import Union, List, Dict
from pathlib import Path
from PIL import Image
from transformers import pipeline
from assignment3.models.base import ModelHandlerBase


class ImageModelHandler(ModelHandlerBase):
    def _build_pipeline(self):
        # Create an image-classification pipeline (top-k returned).
        return pipeline("image-classification", model=self.model_id)

    def _format_output(self, raw_output: List[Dict]) -> str:
        # raw_output is a list of dicts like: [{"label": "...", "score": 0.95}, ...]
        if not raw_output:
            return "No result."

        # Sort by score (desc) and take top 3 for clearer feedback.
        top_preds = sorted(raw_output, key=lambda x: x.get("score", 0.0), reverse=True)[:3]

        lines = ["Predictions:"]
        for pred in top_preds:
            label = pred.get("label", "?")
            score = pred.get("score", 0.0)
            lines.append(f"- {label} (confidence {score:.2f})")
        return "\n".join(lines)

    def process(self, input_data: Union[str, Path, Image.Image]) -> str:
        """
        Accept either a file path or a PIL.Image.Image, run the model, and return formatted text.
        """
        if isinstance(input_data, (str, Path)):
            img = Image.open(input_data).convert("RGB")
        elif isinstance(input_data, Image.Image):
            img = input_data.convert("RGB")
        else:
            raise TypeError("Unsupported input for image model. Provide a file path or PIL.Image.Image.")

        pipe = self._get_pipeline()
        if pipe:
            raw = pipe(img)  # returns list of {label, score}
            return self._format_output(raw)
        return "Empty Input Data"