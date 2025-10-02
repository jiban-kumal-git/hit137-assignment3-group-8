# hit137-assignment3-group-8
Integrate LLM models 
Chosen Hugging models
1. Image Classification
2. Text Classification

HIT137 – Assignment 3 (Group 8)
📌 Project Overview

This project demonstrates how Object-Oriented Programming (OOP) principles can be combined with Hugging Face Transformers and a Tkinter GUI to create a simple interactive application.

Users can:

Run text sentiment analysis on their own input.

Run image classification on selected images.

Explore Model Information and OOP Notes inside the GUI.

This project was built collaboratively by a team of 4 members.

🏗️ Project Structure
assignment3/
│── __init__.py              # Marks package
│── main.py                  # Entry point
│── gui.py                   # Tkinter GUI scaffold (tabs for App, Model Info, OOP Notes)
│── model_info.py            # Text describing chosen ML models
│── oop_explain.py           # Notes explaining OOP principles
│
├── models/
│   ├── base.py              # Abstract base class for models (OOP backbone)
│   ├── text_model.py        # Text sentiment analysis model (Hugging Face)
│   └── image_model.py       # Image classification model (Hugging Face)
│
├── utils/
│   ├── decorators.py        # Logging / timing decorators
│   └── mixins.py            # Error handling + logging mixins
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

⚙️ Setup Instructions

Clone the repository

git clone https://github.com/<your-org-or-username>/hit137-assignment3-group-8.git
cd hit137-assignment3-group-8


Create & activate a virtual environment

python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\activate
# On Git Bash / Linux / Mac:
source .venv/bin/activate


Install dependencies

pip install -r assignment3/requirements.txt

▶️ Running the App

Run the main entry point:

python -m assignment3.main


You will see a GUI window with three tabs:

App → run text or image models.

Model Info → displays details about chosen ML models.

OOP Notes → shows explanations of OOP concepts used.

🤖 Features
Text Sentiment Analysis

Uses Hugging Face pipeline (text-classification).

Example:

Input: "I love this project!"

Output: Sentiment: POSITIVE (confidence 0.98)

Image Classification

Uses Hugging Face Vision Transformer (google/vit-base-patch16-224).

Example:

Input: uploaded image of a dog.

Output: Label: Labrador retriever (confidence 0.92)

OOP Concepts Demonstrated

Encapsulation: private attributes in ModelHandlerBase.

Inheritance: TextModelHandler and ImageModelHandler extend the abstract base.

Polymorphism: each model handler implements its own _build_pipeline() and _format_output().

Mixins/Decorators: logging and error handling cross-cutting features.

👩‍💻 Team Members

Group of 4 students (HIT137).
Each member contributed to different parts: GUI, models, OOP backbone, documentation.

📦 Requirements

Key dependencies:

torch==2.6.0

transformers==4.43.3

huggingface_hub==0.24.6

Pillow==10.4.0

tkinter (standard with Python)

🚀 Future Work

Add support for audio models (speech recognition).

Improve GUI layout (drag & drop for images, dark mode).

Add model selection (choose between multiple HF models dynamically).