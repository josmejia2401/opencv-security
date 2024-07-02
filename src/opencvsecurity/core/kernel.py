#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.opencvsecurity.models.frame_model import FrameModel
from src.opencvsecurity.core.gui.gui import Gui
from src.opencvsecurity.core.gui.camera_default import CameraDefault
from src.opencvsecurity.core.cam_list import cam_list
from src.opencvsecurity.models.video_format_model import VideoFormatModel


import pathlib

class Kernel:

    gui: Gui
    camera_default: CameraDefault
    options: FrameModel
    ids_cam_list: list

    def __init__(self):
        super().__init__()
        self.gui = None
        self.camera_default = None
        self.ids_cam_list = None


    def init(self) -> None:
        self.ids_cam_list = cam_list()
        #320x240, 640x480, 800x480, 1024x600, 1024x768, 1440x900, 1920x1200, 1280x720, 1920x1080, 768x576, 720x480
        self.options = FrameModel(
            #output_path=str(pathlib.Path(__file__).parent.resolve()),
            frame_width=1280,
            frame_height=720,
            frame_fps=30,
            #video_format='MP4V',
            video_format=VideoFormatModel(
                output_path=str(pathlib.Path(__file__).parent.resolve()),
                video_format='MP4V',
                video_height=720,
                video_width=1280,
                video_color=True
            )
        )
        self.gui = Gui(options=self.options, ids_cam_list=self.ids_cam_list)
        self.gui.init()