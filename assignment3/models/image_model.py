# Image classification handler using Hugging Face ViT.

from typing import Union
from pathlib import Path
from PIL import Image
from transformers import pipeline
from assignment3.models.base import ModelHandlerBase

class ImageModelHandler(ModelHandlerBase):
    def _build_pipeline(self):
        # Image classification pipeline (top-1 by default).
        return pipeline("image-classification", model=self.model_id)

    def _format_output(self, raw_output):
        # raw_output is a list of {label, score} dicts.
        if not raw_output:
            return "No result."
        top = raw_output[0]
        label = top.get("label", "?")
        score = top.get("score", 0.0)
        return f"Image label: {label} (confidence {score:.2f})"

    def process(self, input_data: Union[str, Path, Image.Image]):
        # Accept file path or PIL.Image and run prediction.
        if isinstance(input_data, (str, Path)):
            img = Image.open(input_data).convert("RGB")
        elif isinstance(input_data, Image.Image):
            img = input_data.convert("RGB")
        else:
            raise TypeError("Unsupported input for image model.")
        pipe = self._get_pipeline()
        raw = pipe(img)
        return self._format_output(raw)

