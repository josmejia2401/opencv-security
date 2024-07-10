import threading
import queue
import time

from src.core.save_frame import SaveFrame
from src.core.models.frame_model import FrameModel
from src.core.models.proccess_frame_model import ProcessFrameModel
from src.core.sub.sub_worker import SubWorker

class FrameWorker(threading.Thread):
    """
    This thread is for proccess an frame.
    """
    q: queue.Queue
    save_frame: list[type[SaveFrame]]
    options: FrameModel
    subscribers: list[type[SubWorker]]

    def __init__(self, q, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = q
        self.options = options
        self.stopEvent = threading.Event()
        self.save_frame = []
        self.subscribers = []

    def run(self):
        while not self.stopEvent.is_set():
            try:
                data = self.q.get(timeout=3)
                self.save_video(data=data)
                self.send_message(msg=data)
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
            frame_selected = SaveFrame(
                options=self.options,
                source=data.source
            )
            frame_selected.init()
            self.save_frame.append(frame_selected)
        frame_selected.save_video(data.grabbed, data.frame)

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

    def attach(self, clazz: SubWorker):
        try:
            if clazz not in self.subscribers:
                self.subscribers.append(clazz)
        except Exception as e:
            print("[ERROR]", e)

    def detach(self, clazz: SubWorker):
        self.subscribers.remove(clazz)

    def send_message(self, msg: ProcessFrameModel = None):
        for clazz in self.subscribers:
            clazz.on_message(msg)