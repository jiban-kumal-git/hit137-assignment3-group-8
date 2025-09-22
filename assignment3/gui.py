"""
GUI layer for the application.
Right now: a minimal window so you can run the program.
Later: we'll add tabs (App, Model Info, OOP Notes), inputs, and outputs.
"""

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    """
    Main Tkinter application window.
    - Holds the Notebook (tabs) and basic widgets.
    - Will call into model handlers later.
    """
    def __init__(self):
        super().__init__()
        self.title("HIT137 – OOP + Hugging Face (Scaffold)")
        self.geometry("800x500")
        self._build_ui()

    def _build_ui(self):
        """
        Build the initial UI shell:
        - A Notebook with three tabs (empty placeholders for now).
        """
        nb = ttk.Notebook(self)
        self.tab_app = ttk.Frame(nb)
        self.tab_models = ttk.Frame(nb)
        self.tab_oop = ttk.Frame(nb)

        nb.add(self.tab_app, text="App")
        nb.add(self.tab_models, text="Model Info")
        nb.add(self.tab_oop, text="OOP Notes")
        nb.pack(fill=tk.BOTH, expand=True)

        # Basic label so you can see something on screen
        ttk.Label(self.tab_app, text="Hello! The GUI scaffold is running.").pack(pady=20)
