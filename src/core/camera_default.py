#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import queue
from src.core.definitions.camera import Camera, cv2
from src.core.models.proccess_frame_model import ProcessFrameModel

class CameraDefault(Camera):

    q: queue.Queue
    frame = cv2.typing.MatLike
    frame_prev = cv2.typing.MatLike

    def __init__(self, source, options, q):
        super().__init__(source=source, options=options)
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
                    self.q.put(ProcessFrameModel(frame=self.frame, source=self.source, grabbed=grabbed))
                else:
                    break
        except RuntimeError as e:
            print('[ERROR] error', e)
