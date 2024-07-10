#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import tkinter as tk
import random
from PIL import ImageTk, Image
import cv2

from src.core.models.proccess_frame_model import ProcessFrameModel
from src.gui.models.frame_box_model import FrameBoxModel


class DynamicGrid(tk.Frame):
    boxes: dict[str, FrameBoxModel]
    text: tk.Text

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled")
        self.text.pack(fill="both", expand=True)
        self.boxes = {}
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
        frameBox = FrameBoxModel(
            box=box,
            height=height,
            width=width,
            panel=None,
            soure=source,
        )
        self.boxes[source] = frameBox
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")

    def on_message(self, message: ProcessFrameModel):
        if message.source in self.boxes:
            frameBox: FrameBoxModel = self.boxes[message.source]
            image = cv2.cvtColor(message.frame, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(image)
            #image = image.resize((frameBox.width, frameBox.height)) 
            image = ImageTk.PhotoImage(image=image)
            if frameBox.panel is None:
                frameBox.panel = tk.Label(frameBox.box, image=image, width=frameBox.width, height=frameBox.height)
                frameBox.panel.image = image
                frameBox.panel.pack()
            else:
                frameBox.panel.configure(image=image)
                frameBox.panel.image = image
            self.boxes[message.source] = frameBox

    def on_close(self):
        print('[INFO] closing ...')
        for box in self.boxes:
            try:
                self.boxes[box].box.quit()
                self.boxes[box].box.destroy()
            except: pass
        self.quit()
        self.destroy()