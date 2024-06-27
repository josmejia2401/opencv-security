#!/usr/bin/env python3
#!/usr/bin/python3.12.4
# OpenCV 4.10, Raspberry pi 3/3b/4b - test on macOS
from src.opencvsecurity.core.kernel import Kernel

class Application:
    def __init__(self) -> None:
        self.camera = Kernel()
        self.camera.init()
