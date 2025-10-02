"""
GUI layer for the application.
Three tabs: App, Model Info, OOP Notes.
App tab runs sentiment analysis via a TextModelHandler.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from assignment3.model_info import MODEL_INFO
from assignment3.oop_explain import OOP_NOTES
from assignment3.models.text_model import TextModelHandler


class App(tk.Tk):
    """
    Main Tkinter application window.
    Holds the Notebook (tabs) and basic widgets.
    """
    def __init__(self):
        super().__init__()
        self.title("HIT137 – OOP + Hugging Face")
        self.geometry("900x600")

        # simple app state
        self.selected_input = tk.StringVar(value="text")
        self.status_text = tk.StringVar(value="Ready.")
        self.text_handler = None  # lazy init

        self._build_ui()

    def _build_ui(self):
        """
        Build the UI shell:
        - A Notebook with three tabs (App, Model Info, OOP Notes).
        - App tab contains input, output, and status areas.
        """
        notebook = ttk.Notebook(self)

        # tabs
        self.tab_app = ttk.Frame(notebook)
        self.tab_models = ttk.Frame(notebook)
        self.tab_oop = ttk.Frame(notebook)

        notebook.add(self.tab_app, text="App")
        notebook.add(self.tab_models, text="Model Info")
        notebook.add(self.tab_oop, text="OOP Notes")
        notebook.pack(fill=tk.BOTH, expand=True)

        # --- App tab layout ---------------------------------------------------
        app_container = ttk.Frame(self.tab_app, padding=12)
        app_container.pack(fill=tk.BOTH, expand=True)

        # top controls row
        top_row = ttk.Frame(app_container)
        top_row.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(top_row, text="Input type:").pack(side=tk.LEFT)
        ttk.Combobox(
            top_row, state="readonly", values=["text"], width=10,
            textvariable=self.selected_input
        ).pack(side=tk.LEFT, padx=8)

        ttk.Button(top_row, text="Run Text", command=self._run_text).pack(side=tk.LEFT, padx=(8, 0))

        # text input group
        text_group = ttk.LabelFrame(app_container, text="Text Input", padding=8)
        text_group.pack(fill=tk.X, pady=(4, 8))
        self.txt_input = tk.Text(text_group, height=5, wrap="word")
        self.txt_input.pack(fill=tk.X)

        # output group
        out_group = ttk.LabelFrame(app_container, text="Output", padding=8)
        out_group.pack(fill=tk.BOTH, expand=True, pady=8)
        self.output = tk.Text(out_group, height=14, wrap="word")
        self.output.pack(fill=tk.BOTH, expand=True)

        # status row
        status_row = ttk.Frame(app_container)
        status_row.pack(fill=tk.X, pady=(6, 0))
        ttk.Label(status_row, textvariable=self.status_text, anchor="w").pack(side=tk.LEFT)

        # --- Model Info tab ---------------------------------------------------
        self._build_info_tab(self.tab_models)

        # --- OOP Notes tab ----------------------------------------------------
        self._build_oop_tab(self.tab_oop)

    def _build_info_tab(self, parent: ttk.Frame):
        """
        Render selected model metadata in a read-only text box.
        """
        container = ttk.Frame(parent, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Model Info", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        text = tk.Text(container, wrap="word", height=18)
        text.pack(fill=tk.BOTH, expand=True, pady=8)

        # build readable lines from MODEL_INFO
        lines = []
        t = MODEL_INFO.get("text", {})
        i = MODEL_INFO.get("image", {})
        if t:
            lines.append(f"Text model: {t.get('id', '')}")
            lines.append(f"About: {t.get('about', '')}")
            lines.append("")
        if i:
            lines.append(f"Image model: {i.get('id', '')}")
            lines.append(f"About: {i.get('about', '')}")
        text.insert("end", "\n".join(lines))
        text.configure(state="disabled")

    def _build_oop_tab(self, parent: ttk.Frame):
        """
        Render OOP concepts in a read-only text box.
        """
        container = ttk.Frame(parent, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="OOP Notes", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        text = tk.Text(container, wrap="word", height=18)
        text.pack(fill=tk.BOTH, expand=True, pady=8)
        text.insert("end", OOP_NOTES)
        text.configure(state="disabled")

    # ------------------------- actions ---------------------------------------

    def _ensure_text_handler(self):
        """
        Lazily construct the text model handler.
        First call may download model weights.
        """
        if self.text_handler is None:
            model_id = MODEL_INFO["text"]["id"]
            self.status_text.set("Preparing text model… first run may download weights.")
            self.update_idletasks()
            self.text_handler = TextModelHandler(model_id)
            self.status_text.set("Text model ready.")

    def _run_text(self):
        """
        Pull text from input, run sentiment, and print formatted output.
        """
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
        """
        Replace the Output text area with new content.
        """
        self.output.delete("1.0", "end")
        self.output.insert("end", content)
