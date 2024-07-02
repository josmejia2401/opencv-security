#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import tkinter as tk
from PIL import ImageTk, Image
import imutils

from src.opencvsecurity.core.definitions.camera import Camera, cv2
from src.opencvsecurity.core.save_frame import SaveFrame

class CameraDefault(Camera):

    root: tk.Frame
    panel: tk.Label

    _frame = cv2.typing.MatLike
    _frame_prev = cv2.typing.MatLike
    _save_frame: SaveFrame
    _width: int
    _height: int

    def __init__(self, source, options, root, width, height):
        super().__init__(source=source, options=options)
        self.root = root
        self._save_frame = SaveFrame(options=options, source=source)
        self._width = int(width - 1)
        self._height = int(height - 1)
        self._frame = None
        self._frame_prev = None
        self.panel = None

    def init(self) -> None:
        self.init_main()
        
    def on_close(self):
        print('[INFO] closing ...')
        self._save_frame.release()
        self.stop()
        
    def take_snapshot(self):
        self._save_frame.save_image(True, self._frame)

    def video_loop(self) -> None:
        try:
            while not self._stopEvent.is_set():
                grabbed, self._frame = self.read()
                if grabbed:
                    # frame with original dimensions to save
                    self._save_frame.save_video(grabbed, self._frame)
                    # frame with new dimensions to view
                    self._frame = self.resize(self._frame)
                    image = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGBA)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image=image)
                    if self.panel is None:
                        self.panel = tk.Label(self.root, image=image)
                        self.panel.image = image
                        self.panel.pack()
                    else:
                        self.panel.configure(image=image)
                        self.panel.image = image
                else:
                    break
        except RuntimeError as e:
            print('[ERROR] error', e)

    def resize(self, frame) -> any:
        try:
            if frame is None:
                return None
            return cv2.resize(frame, (self._width, self._height))
        except Exception as e:
            return imutils.resize(self._frame, self._width, self._height)
