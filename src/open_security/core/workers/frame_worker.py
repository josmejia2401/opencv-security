import threading
import queue
import time

from src.open_security.core.save_frame import SaveFrame
from src.open_security.models.frame_model import FrameModel
from src.open_security.models.proccess_frame_model import ProcessFrameModel

class FrameWorker(threading.Thread):
    """
    This thread is for proccess an frame.
    """
    q: queue.Queue
    save_frame: list[type[SaveFrame]]
    options: FrameModel

    def __init__(self, q, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = q
        self.options = options
        self.stopEvent = threading.Event()
        self.save_frame = []

    def run(self):
        while not self.stopEvent.is_set():
            try:
                data = self.q.get(timeout=3)
                self.save_video(data=data)
                self.q.task_done()
            except queue.Empty as e:
                print('[ERROR] Empty', e)
            except Exception as e:
                print('[ERROR] Exception', e)
    
    def save_video(self, data: ProcessFrameModel) -> None:
        frame_selected = None
        if len(self.save_frame) > 0:
            for frame in self.save_frame:
                if frame.source == data.source:
                    frame_selected = frame
                    break
        if frame_selected is None:
            frame = SaveFrame(
                options=self.options,
                source=data.source
            )
            frame.init()
            self.save_frame.append(frame)
        frame.save_video(data.grabbed, data.frame)

    def on_close(self) -> None:
        print('[INFO] closing ...')
        try:
            self.stopEvent.set()
            time.sleep(1)
        except Exception as e:
            print('[ERROR]', e)
        try:
            if len(self.save_frame) > 0:
                for frame in self.save_frame:
                    frame.release()
        except Exception as e:
            print('[ERROR]', e)