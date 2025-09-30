# I am using Tkinter to build the GUI.
# For now I only make one window with a single label.
# Later I will add tabs (App, Model Info, OOP Notes) and buttons.

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    # My App class is basically a Tk window.
    def __init__(self):
        # I call the parent constructor to properly set up the window.
        super().__init__()

        # I set a title and a fixed window size.
        self.title("HIT137 – OOP + Hugging Face (Scaffold)")
        self.geometry("800x500")

        # I call my own function to build the user interface.
        self._build_ui()

    def _build_ui(self):
        # I create a simple label to check if the GUI is working.
        ttk.Label(self, text="Hello! The GUI scaffold is running.").pack(pady=24)
