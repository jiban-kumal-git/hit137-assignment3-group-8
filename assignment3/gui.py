# Tkinter GUI with a three-tab layout.
# Tabs: App, Model Info, OOP Notes.

import tkinter as tk
from tkinter import ttk, messagebox

from .model_info import MODEL_INFO
from .oop_explain import OOP_NOTES
from .models.text_model import TextModelHandler

class App(tk.Tk):
    # Main application window derived from tk.Tk.
    def __init__(self):
        super().__init__()
        self.title("HIT137 - OOP + Hugging Face (Skeleton)")
        self.geometry("900x600")

        # State
        self.selected_input = tk.StringVar(value="text")  # "text" | "image"
        self.status_text = tk.StringVar(value="Ready.")
        self.text_handler = None  # lazy init on first use

        self._build_ui()

    def _build_ui(self):
        # Notebook holds multiple tabs inside a single window.
        notebook = ttk.Notebook(self)

        # Create three tabs and add them to the notebook.
        self.tab_app = ttk.Frame(notebook)
        self.tab_models = ttk.Frame(notebook)
        self.tab_oop = ttk.Frame(notebook)

        notebook.add(self.tab_app, text="App")
        notebook.add(self.tab_models, text="Model Info")
        notebook.add(self.tab_oop, text="OOP Notes")
        notebook.pack(fill=tk.BOTH, expand=True)

        # -----------------------
        # App tab
        # -----------------------
        app_container = ttk.Frame(self.tab_app, padding=12)
        app_container.pack(fill=tk.BOTH, expand=True)

        # Row: input type + run buttons
        top_row = ttk.Frame(app_container)
        top_row.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(top_row, text="Input type:").pack(side=tk.LEFT)
        self.cmb_type = ttk.Combobox(
            top_row, state="readonly", values=["text", "image"], width=10,
            textvariable=self.selected_input
        )
        self.cmb_type.pack(side=tk.LEFT, padx=8)

        ttk.Button(top_row, text="Run Text", command=self._run_text).pack(side=tk.LEFT, padx=(8, 0))
        # Image button will be enabled when image model is added later.
        self.btn_run_image = ttk.Button(top_row, text="Run Image (coming soon)", state="disabled")
        self.btn_run_image.pack(side=tk.LEFT, padx=8)

        # Row: text input area (visible for text mode)
        text_group = ttk.LabelFrame(app_container, text="Text Input", padding=8)
        text_group.pack(fill=tk.X, pady=(4, 8))
        self.txt_input = tk.Text(text_group, height=5, wrap="word")
        self.txt_input.pack(fill=tk.X)

        # Output area
        out_group = ttk.LabelFrame(app_container, text="Output", padding=8)
        out_group.pack(fill=tk.BOTH, expand=True, pady=8)
        self.output = tk.Text(out_group, height=14, wrap="word")
        self.output.pack(fill=tk.BOTH, expand=True)

        # Status bar
        status_row = ttk.Frame(app_container)
        status_row.pack(fill=tk.X, pady=(6, 0))
        ttk.Label(status_row, textvariable=self.status_text, anchor="w").pack(side=tk.LEFT)

        # -----------------------
        # Model Info tab
        # -----------------------
        models_container = ttk.Frame(self.tab_models, padding=12)
        models_container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(models_container, text="Model Info", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.model_info_text = tk.Text(models_container, height=18, wrap="word")
        self.model_info_text.pack(fill=tk.BOTH, expand=True, pady=8)

        info_lines = []
        t = MODEL_INFO["text"]
        info_lines.append(f"Text model: {t['id']}")
        info_lines.append(f"About: {t['about']}")
        # Image model info remains visible even before wiring image logic.
        i = MODEL_INFO["image"]
        info_lines.append("")
        info_lines.append(f"Image model: {i['id']}")
        info_lines.append(f"About: {i['about']}")
        self.model_info_text.insert("end", "\n".join(info_lines))
        self.model_info_text.configure(state="disabled")

        # -----------------------
        # OOP Notes tab
        # -----------------------
        oop_container = ttk.Frame(self.tab_oop, padding=12)
        oop_container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(oop_container, text="OOP Notes", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.oop_text = tk.Text(oop_container, height=18, wrap="word")
        self.oop_text.pack(fill=tk.BOTH, expand=True, pady=8)
        self.oop_text.insert("end", OOP_NOTES)
        self.oop_text.configure(state="disabled")

    # -----------------------
    # Actions
    # -----------------------
    def _ensure_text_handler(self):
        # Lazily create the text model handler (first call triggers model download).
        if self.text_handler is None:
            model_id = MODEL_INFO["text"]["id"]
            self.status_text.set("Preparing text model… first run may download weights.")
            self.update_idletasks()
            self.text_handler = TextModelHandler(model_id)
            self.status_text.set("Text model ready.")

    def _run_text(self):
        # Validate input, ensure handler, run inference, print to Output.
        text = self.txt_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Input required", "Enter some text for analysis.")
            return
        try:
            self._ensure_text_handler()
            self.status_text.set("Running sentiment…")
            self.update_idletasks()
            result = self.text_handler.process(text)
            self._set_output(result)
            self.status_text.set("Done.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_text.set("Failed. See console for details.")

    def _set_output(self, content: str):
        # Replace output content.
        self.output.delete("1.0", "end")
        self.output.insert("end", content)
