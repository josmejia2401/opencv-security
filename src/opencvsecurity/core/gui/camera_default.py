#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import tkinter as tk
from PIL import ImageTk, Image
import imutils

from src.opencvsecurity.core.definitions.camera import Camera, cv2
from src.opencvsecurity.core.save_frame import SaveFrame

class CameraDefault(Camera):

    root: tk.Tk
    panel: tk.Label

    _frame = cv2.typing.MatLike
    _save_frame: SaveFrame

    def __init__(self, options, root, save_frame):
        super().__init__(options=options)
        self.root = root
        self._save_frame = save_frame
        self._frame = None
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
                    self._save_frame.save_video(grabbed, self._frame)
                    
                    self._frame = imutils.resize(self._frame, width=self._options.frame_width, height=self._options.frame_height)

                    image = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGBA)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image=image)
                    if self.panel is None:
                        self.panel = tk.Label(self.root, image=image)
                        self.panel.image = image
                        self.panel.pack(side='left', padx=10, pady=10)
                    else:
                        self.panel.configure(image=image)
                        self.panel.image = image
                else:
                    break
        except RuntimeError as e:
            print('[ERROR] error', e)