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

    def __init__(self, source, options, root):
        super().__init__(source=source, options=options)
        self.root = root
        self._save_frame = SaveFrame(options=options, source=source)
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
                    self._frame = self.resize(self._frame)
                    self._save_frame.save_video(grabbed, self._frame)
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

    #320x240, 640x480, 800x480, 1024x600, 1024x768, 1440x900, 1920x1200, 1280x720, 1920x1080, 768x576, 720x480
    def resize(self, frame) -> any:
        try:
            if frame is None:
                return None
            return cv2.resize(frame, (self._options.frame_width, self._options.frame_height))
        except Exception as e:
            return imutils.resize(self._frame, width=self._options.frame_width, height=self._options.frame_height)
