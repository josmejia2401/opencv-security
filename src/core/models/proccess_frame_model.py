#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass
import cv2

@dataclass
class ProcessFrameModel:
    frame: cv2.typing.MatLike
    source: int
    grabbed: bool
