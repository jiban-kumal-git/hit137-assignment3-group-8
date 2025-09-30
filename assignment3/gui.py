# Tkinter GUI with a three-tab layout.
# Tabs: App, Model Info, OOP Notes.

import tkinter as tk
from tkinter import ttk

from assignment3.model_info import MODEL_INFO
from assignment3.oop_explain import OOP_NOTES

class App(tk.Tk):
    # Main application window derived from tk.Tk.
    def __init__(self):
        super().__init__()
        self.title("HIT137 – OOP + Hugging Face (Skeleton)")
        self.geometry("900x600")
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
        # App tab (placeholders)
        # -----------------------
        app_container = ttk.Frame(self.tab_app, padding=12)
        app_container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            app_container,
            text="App tab: inputs and outputs will be added here."
        ).pack(anchor="w", pady=(0, 8))

        top_row = ttk.Frame(app_container)
        top_row.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(top_row, text="Input type:").pack(side=tk.LEFT)
        ttk.Combobox(top_row, state="readonly", values=["text", "image"], width=10).pack(side=tk.LEFT, padx=8)
        ttk.Button(top_row, text="Run").pack(side=tk.LEFT)

        out_group = ttk.LabelFrame(app_container, text="Output", padding=8)
        out_group.pack(fill=tk.BOTH, expand=True, pady=12)
        self.output = tk.Text(out_group, height=12, wrap="word")
        self.output.pack(fill=tk.BOTH, expand=True)

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
        i = MODEL_INFO["image"]
        info_lines.append(f"Text model: {t['id']}")
        info_lines.append(f"About: {t['about']}")
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
