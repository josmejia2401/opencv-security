#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass
from src.core.models.video_format_model import VideoFormatModel

@dataclass
class FrameModel:
    frame_width: int
    frame_height: int
    frame_fps: int
    video_format: VideoFormatModel
