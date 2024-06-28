#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import cv2
import tkinter as tk
import time
from src.opencvsecurity.core.save_frame import SaveFrame
from src.opencvsecurity.core.gui.camera_default import CameraDefault
from src.opencvsecurity.models.frame_model import FrameModel
from src.opencvsecurity.core.gui.dynamic_grid import DynamicGrid

class Gui:

    root: tk.Tk
    panel: tk.Label
    frame: cv2.typing.MatLike
    options: FrameModel
    ids_cam_list: list
    cam_list: list

    def __init__(self, options, ids_cam_list):
        super().__init__()
        self.root = None
        self.panel = None
        self.frame = None
        self.options = options
        self.ids_cam_list = ids_cam_list
        self.cam_list = None

    def init(self) -> None:
        self.cam_list = []
        self.root = tk.Tk()
        self.root.update_idletasks()
        self.root.attributes('-fullscreen', True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(screen_width, screen_height))
        self.root.title('Login')
        self.root.resizable(0, 0)

        self.dynamic_grid = DynamicGrid(parent=self.root, width=screen_width, height=screen_height)
        self.dynamic_grid.pack(side="top", fill="both", expand=True)

        # add a few boxes to start
        if len(self.ids_cam_list) == 1:
            self.dynamic_grid.add_box(
                color='red',
                width=screen_width,
                height=screen_height,
                source=0,
                options=self.options)
        if len(self.ids_cam_list) == 2:
            width = screen_width/2
            height = screen_height
            self.dynamic_grid.add_box(color='red', width=width, height=height, source=0, options=self.options)
            self.dynamic_grid.add_box(color='black', width=width, height=height, source=1, options=self.options)
        if len(self.ids_cam_list) == 3:
            width = screen_width/2 - 1
            height = screen_height / 2
            self.dynamic_grid.add_box(color='red', width=width, height=height, source=0, options=self.options)
            self.dynamic_grid.add_box(color='black', width=width, height=height, source=1, options=self.options)
            self.dynamic_grid.add_box(width=screen_width, height=height, source=2, options=self.options)

        if len(self.ids_cam_list) == 4:
            width = screen_width/3 - 1
            height = screen_height/2
            self.dynamic_grid.add_box(width=width, height=height, source=0, options=self.options)
            self.dynamic_grid.add_box(width=width, height=height, source=1, options=self.options)
            self.dynamic_grid.add_box(width=width, height=height, source=2, options=self.options)
            self.dynamic_grid.add_box(width=screen_width, height=height, source=3, options=self.options)

        #self.root.columnconfigure(0, weight=1)
        #self.root.columnconfigure(0, weight=1)


        #btn = tk.Button(self.root, text='Snapshot!', command=self.camera_default.take_snapshot)
        #btn = tk.Button(self.root, text='Snapshot!')
        #btn.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        self.root.wm_title('Title')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)

        self.root.mainloop()
        
   
    def on_close(self):
        print('[INFO] closing ...')
        for cam in self.cam_list:
            try:
                cam.on_close()
            except: pass
        self.root.quit()
        self.root.destroy()
