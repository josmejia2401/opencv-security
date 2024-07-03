#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import tkinter as tk
import queue
import random
from src.open_security.core.gui.camera_default import CameraDefault
from src.open_security.models.frame_model import FrameModel

class DynamicGrid(tk.Frame):
    cameras: list[type[CameraDefault]]
    options: FrameModel
    q: queue.Queue
    boxes: list[type[tk.Frame]]
    text: tk.Text

    def __init__(self, parent, options, q, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.options = options
        self.q = q
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled")
        self.text.pack(fill="both", expand=True)
        self.boxes = []
        self.cameras = []

    def add_box(self, color=None, width=100, height=100, source = 0):
        bg = color if color else random.choice(("red", "orange", "green", "blue", "violet", "gray"))
        box = tk.Frame(
            self.text,
            bd=1,
            relief="sunken",
            background=bg,
            width=width,
            height=height
        )
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")
        
        camera_default = CameraDefault(
            source=source,
            options=self.options,
            root=box,
            width=width,
            height=height,
            q=self.q
        )
        camera_default.init()
        self.cameras.append(camera_default)

    def on_close(self):
        print('[INFO] closing ...')
        for cam in self.cameras:
            try:
                cam.on_close()
            except: pass
        for box in self.boxes:
            try:
                box.quit()
                box.destroy()
            except: pass
        self.quit()
        self.destroy()