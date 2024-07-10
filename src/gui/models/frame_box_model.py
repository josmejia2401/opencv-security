#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass
import tkinter as tk

@dataclass
class FrameBoxModel:
    box: tk.Frame
    panel: tk.Label
    width: int
    height: int
    soure: int