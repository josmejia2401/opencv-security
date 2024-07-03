#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import tkinter as tk
from PIL import ImageTk, Image
import imutils
import queue
from src.opencvsecurity.core.definitions.camera import Camera, cv2
from src.opencvsecurity.models.proccess_frame_model import ProcessFrameModel

class CameraDefault(Camera):

    root: tk.Frame
    panel: tk.Label
    q: queue.Queue

    frame = cv2.typing.MatLike
    frame_prev = cv2.typing.MatLike
    width: int
    height: int

    def __init__(self, source, options, q, root, width, height):
        super().__init__(source=source, options=options)
        self.root = root
        self.width = int(width - 1)
        self.height = int(height - 1)
        self.q = q
        self.frame = None
        self.frame_prev = None
        self.panel = None

    def init(self) -> None:
        self.init_main()
        
    def on_close(self):
        print('[INFO] closing ...')
        self.stop()

    def video_loop(self) -> None:
        try:
            while not self.stopEvent.is_set():
                grabbed, self.frame = self.read()
                if grabbed:
                    # frame with original dimensions to save
                    self.q.put(ProcessFrameModel(frame=self.frame, source=self.source, grabbed=grabbed))
                    self.frame = self.resize(self.frame)
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
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
            return cv2.resize(frame, (self.width, self.height))
        except Exception as e:
            return imutils.resize(frame, self.width, self.height)
