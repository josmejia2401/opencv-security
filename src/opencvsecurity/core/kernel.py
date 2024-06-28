#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.opencvsecurity.models.frame_model import FrameModel
from src.opencvsecurity.core.gui.gui import Gui
from src.opencvsecurity.core.gui.camera_default import CameraDefault
from src.opencvsecurity.core.cam_list import cam_list

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
        self.ids_cam_list = [0, 1, 2, 3] #cam_list()
        self.options = FrameModel(
            output_path=str(pathlib.Path(__file__).parent.resolve()),
            frame_width=320,
            frame_height=240,
            frame_fps=30,
            video_format='MP4V'
        )
        self.gui = Gui(options=self.options, ids_cam_list=self.ids_cam_list)
        self.gui.init()