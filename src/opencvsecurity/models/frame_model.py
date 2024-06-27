#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass

@dataclass
class FrameModel:
    source: int
    video_format: str
    frame_width: int
    frame_height: int
    frame_fps: int
    output_path: str
