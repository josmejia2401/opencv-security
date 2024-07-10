#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.core.camera_async import CameraAsync
from src.gui.dynamic_grid import DynamicGrid

import tkinter as tk
import cv2

class Kernel:

    _camera_async: CameraAsync
    root: tk.Tk
    panel: tk.Label
    frame: cv2.typing.MatLike
    dynamic_grid = DynamicGrid
    screen_width: int
    screen_height: int

    def __init__(self):
        super().__init__()
        self._camera_async = CameraAsync()
        self.root = None
        self.panel = None
        self.frame = None
        self.dynamic_grid = None
        self.screen_width = None
        self.screen_height = None

    def init_root_gui(self) -> None:
        self.root = tk.Tk()
        self.root.update_idletasks()
        self.root.attributes('-fullscreen', True)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(self.screen_width, self.screen_height))
        self.root.title('OPEN_SECURITY')
        self.root.resizable(0, 0)

    def init_dynamic_grid(self) -> None:
        self.dynamic_grid = DynamicGrid(parent=self.root, width=self.screen_width, height=self.screen_height)
        self.dynamic_grid.pack(side="top", fill="both", expand=True)

    def configure_frames(self) -> None:
         # add a few boxes to start
        if len(self.camera_async.cameras_available) == 1:
            self.dynamic_grid.add_box(width=self.screen_width, height=self.screen_height, source=0)
        elif len(self.camera_async.cameras_available) == 2:
            width = self.screen_width/2
            height = self.screen_height
            self.dynamic_grid.add_box(width=width, height=height, source=0)
            self.dynamic_grid.add_box(width=width,height=height,source=1)
        elif len(self.camera_async.cameras_available) == 3:
            width = self.screen_width/2 - 1
            height = self.screen_height / 2
            self.dynamic_grid.add_box(width=width, height=height, source=0)
            self.dynamic_grid.add_box(width=width, height=height, source=1)
            self.dynamic_grid.add_box(width=self.screen_width, height=height, source=2)
        elif len(self.camera_async.cameras_available) == 4:
            width = self.screen_width/3 - 1
            height = self.screen_height/2
            self.dynamic_grid.add_box(width=width, height=height, source=0)
            self.dynamic_grid.add_box(width=width, height=height, source=1)
            self.dynamic_grid.add_box(width=width, height=height, source=2)
            self.dynamic_grid.add_box(width=self.screen_width, height=height, source=3)

    def init(self) -> None:
        self.init_root_gui()
        self.init_dynamic_grid()
        self.configure_frames()

        self.camera_async.init()
        self.camera_async.frame_worker.attach(clazz=self.dynamic_grid)
        self.camera_async.start()

        self.root.wm_title('OPEN_SECURITY')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.mainloop()
   
    def on_close(self):
        print('[INFO] closing ...')
        self.camera_async.on_close()
        self.dynamic_grid.on_close()
        self.root.quit()
        self.root.destroy()

    @property
    def camera_async(self):
        return self._camera_async