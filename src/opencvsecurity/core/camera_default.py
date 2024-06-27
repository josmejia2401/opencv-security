#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.opencvsecurity.core.definitions.camera import Camera, cv2
from src.opencvsecurity.core.save_frame import SaveFrame
from src.opencvsecurity.core.gui import Gui
import threading

class CameraDefault(Camera):

    _gui: Gui
    _frame = cv2.typing.MatLike
    _thread = threading.Thread
    _stopEvent = threading.Event
    _save_frame: SaveFrame

    def __init__(self, options, gui, save_frame):
        super().__init__(options=options)
        self._frame = None
        self._thread = None
        self._stopEvent = None
        self._save_frame = save_frame
        self._gui = gui

    def init(self) -> None:
        self.init_now()
        self._stopEvent = threading.Event()
        self._thread = threading.Thread(target=self.video_loop, args=())
        self._thread.start()
        
    def on_close(self):
        print('[INFO] closing ...')
        self._stopEvent.set()
        self.stop()

    def video_loop(self) -> None:
        try:
            while not self._stopEvent.is_set():
                grabbed, self._frame = self.read()
                if grabbed:
                    self._save_frame.save_video(grabbed, self._frame)
                    self._gui.draw_frame(frame=self._frame)
                    #self._frame = imutils.resize(self._frame, width=self._options.frame_width, height=self._options.frame_height)
                else:
                    break
        except RuntimeError as e:
            print('[ERROR] error', e)