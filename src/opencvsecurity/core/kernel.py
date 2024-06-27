#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.opencvsecurity.models.frame_model import FrameModel
from src.opencvsecurity.core.gui import Gui
from src.opencvsecurity.core.camera_default import CameraDefault
from src.opencvsecurity.core.save_frame import SaveFrame

import pathlib

class Kernel:

    gui: Gui
    camera_default: CameraDefault
    options: FrameModel
    save_frame: SaveFrame

    def __init__(self):
        super().__init__()
        self.gui = None
        self.camera_default = None
        self.save_frame = None


    def init(self) -> None:
        self.options = FrameModel(
            output_path=str(pathlib.Path(__file__).parent.resolve()),
            frame_width=640,
            frame_height=480,
            frame_fps=30,
            source=0,
            video_format='MP4V'
        )
        self.save_frame = SaveFrame(options=self.options)
        self.gui = Gui(save_frame=self.save_frame)
        self.camera_default = CameraDefault(self.options, self.gui, self.save_frame)
        self.camera_default.init()
        self.gui.init(self.camera_default.on_close)