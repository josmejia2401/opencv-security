#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import cv2
import tkinter as tk
from src.opencvsecurity.core.save_frame import SaveFrame
from src.opencvsecurity.core.gui.camera_default import CameraDefault
from src.opencvsecurity.models.frame_model import FrameModel

class Gui:

    root: tk.Tk
    panel: tk.Label
    save_frame: SaveFrame
    frame: cv2.typing.MatLike
    options: FrameModel


    def __init__(self, options, save_frame):
        super().__init__()
        self.root = None
        self.panel = None
        self.frame = None
        self.options = options
        self.save_frame = save_frame

    def init(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("500x500")

        self.camera_default = CameraDefault(self.options, self.root, self.save_frame)

        btn = tk.Button(self.root, text='Snapshot!', command=self.camera_default.take_snapshot)
        btn.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        self.root.wm_title('Title')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)

        self.camera_default.init()
        self.root.mainloop()
        
   
    def on_close(self):
        print('[INFO] closing ...')
        self.camera_default.on_close()
        self.root.quit()