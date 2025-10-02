"""
GUI layer for the application.
Minimal window with three tabs (App, Model Info, OOP Notes).
"""

import tkinter as tk
from tkinter import ttk

from assignment3.model_info import MODEL_INFO
from assignment3.oop_explain import OOP_NOTES


class App(tk.Tk):
    """
    Main Tkinter application window.
    Holds the Notebook (tabs) and basic widgets.
    """
    def __init__(self):
        super().__init__()
        self.title("HIT137 – OOP + Hugging Face (Scaffold)")
        self.geometry("800x500")
        self._build_ui()

    def _build_ui(self):
        """
        Build the initial UI shell:
        - A Notebook with three tabs.
        """
        nb = ttk.Notebook(self)
        self.tab_app = ttk.Frame(nb)
        self.tab_models = ttk.Frame(nb)
        self.tab_oop = ttk.Frame(nb)

        nb.add(self.tab_app, text="App")
        nb.add(self.tab_models, text="Model Info")
        nb.add(self.tab_oop, text="OOP Notes")
        nb.pack(fill=tk.BOTH, expand=True)

        # --- App tab: simple placeholder for now ---
        ttk.Label(self.tab_app, text="App tab ready. Inputs and outputs will be added here.").pack(pady=16)

        # --- Model Info tab: render model metadata ---
        self._build_info_tab(self.tab_models)

        # --- OOP Notes tab: render OOP explanation text ---
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

        # Build readable lines from MODEL_INFO
        lines = []
        t = MODEL_INFO.get("text", {})
        i = MODEL_INFO.get("image", {})
        if t:
            lines.append(f"Text model: {t.get('id','')}")
            lines.append(f"About: {t.get('about','')}")
            lines.append("")
        if i:
            lines.append(f"Image model: {i.get('id','')}")
            lines.append(f"About: {i.get('about','')}")
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
