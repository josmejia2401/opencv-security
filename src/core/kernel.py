#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.core.models.frame_model import FrameModel
from src.core.cam_list import cam_list
from src.core.models.video_format_model import VideoFormatModel
from src.core.workers.frame_worker import FrameWorker
from src.core.camera_default import CameraDefault


import cv2
import queue
import pathlib

class Kernel:
    options: FrameModel
    frame_worker: FrameWorker
    cameras_attach: list[type[CameraDefault]]

    frame: cv2.typing.MatLike
    cameras_available: list[type[int]]
    q: queue.Queue
    screen_width: int
    screen_height: int

    def __init__(self):
        super().__init__()
        self.cameras_available = []
        self.frame = None
        self.options = None
        self.screen_width = None
        self.screen_height = None
        self.q = queue.Queue()
        self.cameras_attach = []

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
        self.frame_worker.start()

    def init_camera(self):
        for cam in self.cameras_available:
            camera_default = CameraDefault(
                source=cam,
                height=self.screen_height,
                width=self.screen_width,
                options=self.options,
                q=self.q
            )
            self.cameras_attach.append(camera_default)

    def init(self) -> None:
        self.cameras_available = cam_list()
        self.init_options()
        self.init_workers()
   
    def on_close(self):
        print('[INFO] closing ...')
        self.frame_worker.on_close()
        for cam in self.cameras_attach:
            cam.on_close()