#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass

@dataclass
class VideoFormatModel:
    video_format: str
    video_width: int
    video_height: int
    output_path: str
    video_color: bool
