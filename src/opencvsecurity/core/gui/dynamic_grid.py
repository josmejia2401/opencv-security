#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import tkinter as tk
import cv2

from src.opencvsecurity.core.save_frame import SaveFrame
from src.opencvsecurity.core.gui.camera_default import CameraDefault

import random

class DynamicGrid(tk.Frame):
    _frame = cv2.typing.MatLike
    _frame_prev = cv2.typing.MatLike
    _save_frame: SaveFrame


    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled")
        self.text.pack(fill="both", expand=True)
        self.boxes = []
        self.cameras = []

    def add_box(self, color=None, width=100, height=100, source = 0, options = None):

        bg = color if color else random.choice(("red", "orange", "green", "blue", "violet"))
        box = tk.Frame(self.text,
                       bd=1,
                       relief="sunken",
                       background=bg,
                       width=width,
                       height=height)
        
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")

        #self.text.window_create(tk.END, window = tk.Label(self.text, text="jose")) # Example 2


        camera_default = CameraDefault(source=source, options=options, root=box)
        camera_default.init()
        self.cameras.append(camera_default)