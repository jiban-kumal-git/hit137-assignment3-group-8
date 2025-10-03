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
        # Create an image-classification pipeline using the specified model ID.
        # This pipeline will be used to make predictions on images.
        return pipeline("image-classification", model=self.model_id)

    def _format_output(self, raw_output: List[Dict]) -> str:
        # Format the raw output from the pipeline into a readable string.
        # raw_output is a list of dicts like: [{"label": "...", "score": 0.95}, ...]
        if not raw_output:
            return "No result."

        # Sort predictions by confidence score in descending order and select the top 3.
        top_preds = sorted(raw_output, key=lambda x: x.get("score", 0.0), reverse=True)[:3]

        # Build a list of formatted prediction strings.
        lines = ["Predictions:"]
        for pred in top_preds:
            label = pred.get("label", "?")
            score = pred.get("score", 0.0)
            lines.append(f"- {label} (confidence {score:.2f})")
        return "\n".join(lines)

    def process(self, input_data: Union[str, Path, Image.Image]) -> str:
        """
        Accept either a file path or a PIL.Image.Image, run the model, and return formatted text.

        Args:
            input_data: The input image, either as a file path (str/Path) or a PIL.Image.Image object.

        Returns:
            str: Formatted prediction results.
        """
        # Load the image from file path or use the provided PIL Image.
        if isinstance(input_data, (str, Path)):
            img = Image.open(input_data).convert("RGB")
        elif isinstance(input_data, Image.Image):
            img = input_data.convert("RGB")
        else:
            # Raise an error if the input type is unsupported.
            raise TypeError("Unsupported input for image model. Provide a file path or PIL.Image.Image.")

        # Get the image classification pipeline.
        pipe = self._get_pipeline()
        if pipe:
            # Run the pipeline on the image and format the output.
            raw = pipe(img)  # returns list of {label, score}
            return self._format_output(raw)
        # Return a message if the pipeline is not available.
        return "Empty Input Data"