#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.open_security.models.frame_model import FrameModel
from src.open_security.core.cam_list import cam_list
from src.open_security.models.video_format_model import VideoFormatModel
from src.open_security.core.workers.frame_worker import FrameWorker
from src.open_security.core.gui.dynamic_grid import DynamicGrid

import tkinter as tk
import cv2
import queue
import pathlib

class Kernel:

    options: FrameModel
    frame_worker: FrameWorker

    root: tk.Tk
    panel: tk.Label
    frame: cv2.typing.MatLike
    dynamic_grid = DynamicGrid
    cameras_available: list[type[int]]
    q: queue.Queue
    screen_width: int
    screen_height: int

    def __init__(self):
        super().__init__()
        self.cameras_available = []
        self.root = None
        self.panel = None
        self.frame = None
        self.dynamic_grid = None
        self.options = None
        self.screen_width = None
        self.screen_height = None
        self.q = queue.Queue()

    def init_options(self) -> None:
        #320x240, 640x480, 800x480, 1024x600, 1024x768, 1440x900, 1920x1200, 1280x720, 1920x1080, 768x576, 720x480
        self.options = FrameModel(
            frame_width=1280,
            frame_height=720,
            frame_fps=10, #30, 60, 120
            video_format=VideoFormatModel(
                output_path=str(pathlib.Path(__file__).parent.resolve()),
                video_format='mp4v',
                video_height=480,
                video_width=720,
                video_color=True
            )
        )

    def init_workers(self):
        self.frame_worker = FrameWorker(q=self.q, options=self.options)

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
        self.dynamic_grid = DynamicGrid(
            parent=self.root,
            options=self.options,
            q=self.q,
            width=self.screen_width,
            height=self.screen_height
        )
        self.dynamic_grid.pack(side="top", fill="both", expand=True)

    def configure_frames(self) -> None:
         # add a few boxes to start
        if len(self.cameras_available) == 1:
            self.dynamic_grid.add_box(width=self.screen_width, height=self.screen_height, source=0)
        elif len(self.cameras_available) == 2:
            width = self.screen_width/2
            height = self.screen_height
            self.dynamic_grid.add_box(width=width, height=height, source=0)
            self.dynamic_grid.add_box(width=width,height=height,source=1)
        elif len(self.cameras_available) == 3:
            width = self.screen_width/2 - 1
            height = self.screen_height / 2
            self.dynamic_grid.add_box(width=width, height=height, source=0)
            self.dynamic_grid.add_box(width=width, height=height, source=1)
            self.dynamic_grid.add_box(width=self.screen_width, height=height, source=2)
        elif len(self.cameras_available) == 4:
            width = self.screen_width/3 - 1
            height = self.screen_height/2
            self.dynamic_grid.add_box(width=width, height=height, source=0)
            self.dynamic_grid.add_box(width=width, height=height, source=1)
            self.dynamic_grid.add_box(width=width, height=height, source=2)
            self.dynamic_grid.add_box(width=self.screen_width, height=height, source=3)

    def init(self) -> None:
        self.cameras_available = cam_list()
        self.init_options()
        self.init_workers()
        self.init_root_gui()
        self.init_dynamic_grid()
        self.configure_frames()

        self.frame_worker.start()

        self.root.wm_title('OPEN_SECURITY')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.mainloop()
   
    def on_close(self):
        print('[INFO] closing ...')
        self.frame_worker.on_close()
        self.dynamic_grid.on_close()
        self.root.quit()
        self.root.destroy()