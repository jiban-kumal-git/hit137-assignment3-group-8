"""
GUI layer for the application.
Three tabs: App, Model Info, OOP Notes.
App tab supports sentiment on text and classification on images.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

from assignment3.model_info import MODEL_INFO
from assignment3.oop_explain import OOP_NOTES
from assignment3.models.text_model import TextModelHandler
from assignment3.models.image_model import ImageModelHandler


class App(tk.Tk):
    """
    Main Tkinter window with a Notebook and action handlers.
    """
    def __init__(self):
        super().__init__()
        self.title("HIT137 – OOP + Hugging Face")
        self.geometry("1000x650")

        # simple state
        self.selected_input = tk.StringVar(value="text")
        self.status_text = tk.StringVar(value="Ready.")
        self.text_handler = None         # created lazily
        self.image_handler = None        # created lazily
        self._img_path = None            # selected image path
        self._img_preview = None         # reference to PhotoImage (avoid GC)

        self._build_ui()

    def _build_ui(self):
        """
        Build tabs and widgets.
        """
        notebook = ttk.Notebook(self)

        self.tab_app = ttk.Frame(notebook)
        self.tab_models = ttk.Frame(notebook)
        self.tab_oop = ttk.Frame(notebook)

        notebook.add(self.tab_app, text="App")
        notebook.add(self.tab_models, text="Model Info")
        notebook.add(self.tab_oop, text="OOP Notes")
        notebook.pack(fill=tk.BOTH, expand=True)

        # ---- App tab --------------------------------------------------------
        app_container = ttk.Frame(self.tab_app, padding=12)
        app_container.pack(fill=tk.BOTH, expand=True)

        # top controls
        top_row = ttk.Frame(app_container)
        top_row.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(top_row, text="Input type:").pack(side=tk.LEFT)
        ttk.Combobox(
            top_row, state="readonly", values=["text", "image"], width=10,
            textvariable=self.selected_input
        ).pack(side=tk.LEFT, padx=8)

        ttk.Button(top_row, text="Open Image…", command=self._pick_image).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(top_row, text="Run Text", command=self._run_text).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(top_row, text="Run Image", command=self._run_image).pack(side=tk.LEFT, padx=(8, 0))

        # text input
        text_group = ttk.LabelFrame(app_container, text="Text Input", padding=8)
        text_group.pack(fill=tk.X, pady=(4, 8))
        self.txt_input = tk.Text(text_group, height=6, wrap="word")
        self.txt_input.pack(fill=tk.X)

        # image preview
        img_group = ttk.LabelFrame(app_container, text="Image Preview", padding=8)
        img_group.pack(fill=tk.X, pady=(4, 8))
        self.img_canvas = tk.Canvas(img_group, width=320, height=320, bg="#f0f0f0", highlightthickness=1)
        self.img_canvas.pack()

        # output area
        out_group = ttk.LabelFrame(app_container, text="Output", padding=8)
        out_group.pack(fill=tk.BOTH, expand=True, pady=8)
        self.output = tk.Text(out_group, height=12, wrap="word")
        self.output.pack(fill=tk.BOTH, expand=True)

        # status
        status_row = ttk.Frame(app_container)
        status_row.pack(fill=tk.X, pady=(6, 0))
        ttk.Label(status_row, textvariable=self.status_text, anchor="w").pack(side=tk.LEFT)

        # ---- Model Info tab --------------------------------------------------
        self._build_info_tab(self.tab_models)

        # ---- OOP Notes tab ---------------------------------------------------
        self._build_oop_tab(self.tab_oop)

    def _build_info_tab(self, parent: ttk.Frame):
        """
        Render model metadata in a read-only text widget.
        """
        container = ttk.Frame(parent, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Model Info", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        text = tk.Text(container, wrap="word", height=20)
        text.pack(fill=tk.BOTH, expand=True, pady=8)

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
        Render OOP concepts in a read-only text widget.
        """
        container = ttk.Frame(parent, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="OOP Notes", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        text = tk.Text(container, wrap="word", height=20)
        text.pack(fill=tk.BOTH, expand=True, pady=8)
        text.insert("end", OOP_NOTES)
        text.configure(state="disabled")

    # --------------------------- helpers -------------------------------------

    def _set_output(self, content: str):
        """
        Replace the output text area with new content.
        """
        self.output.delete("1.0", "end")
        self.output.insert("end", content)

    # --------------------------- text model ----------------------------------

    def _ensure_text_handler(self):
        """
        Create the text handler on first use.
        """
        if self.text_handler is None:
            model_id = MODEL_INFO["text"]["id"]
            self.status_text.set("Preparing text model… first run may download weights.")
            self.update_idletasks()
            self.text_handler = TextModelHandler(model_id)
            self.status_text.set("Text model ready.")

    def _run_text(self):
        """
        Read input text, run sentiment, and display formatted output.
        """
        content = self.txt_input.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Input required", "Enter some text for analysis.")
            return
        try:
            self._ensure_text_handler()
            self.status_text.set("Running sentiment…")
            self.update_idletasks()
            result = self.text_handler.process(content)
            self._set_output(result)
            self.status_text.set("Done.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_text.set("Failed. See console for details.")

    # --------------------------- image model ---------------------------------

    def _ensure_image_handler(self):
        """
        Create the image handler on first use.
        """
        if self.image_handler is None:
            model_id = MODEL_INFO["image"]["id"]
            self.status_text.set("Preparing image model… first run may download weights.")
            self.update_idletasks()
            self.image_handler = ImageModelHandler(model_id)
            self.status_text.set("Image model ready.")

    def _pick_image(self):
        """
        Open file dialog, load image, and show preview on the canvas.
        """
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
        )
        if not path:
            return
        self._img_path = path
        try:
            img = Image.open(path).convert("RGB")
            img.thumbnail((320, 320))
            self._img_preview = ImageTk.PhotoImage(img)
            self.img_canvas.delete("all")
            self.img_canvas.create_image(160, 160, image=self._img_preview)
            self.status_text.set(f"Selected: {path}")
        except Exception as e:
            messagebox.showerror("Image error", str(e))
            self.status_text.set("Failed to load image.")

    def _run_image(self):
        """
        Classify the selected image and display the top label.
        """
        if not self._img_path:
            messagebox.showwarning("No image", "Choose an image first (Open Image…).")
            return
        try:
            self._ensure_image_handler()
            self.status_text.set("Running image classification…")
            self.update_idletasks()
            result = self.image_handler.process(self._img_path)
            self._set_output(result)
            self.status_text.set("Done.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_text.set("Failed. See console for details.")
