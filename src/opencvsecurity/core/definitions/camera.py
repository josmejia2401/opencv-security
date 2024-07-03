#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import cv2
from abc import ABC, abstractmethod
import threading
import time

from src.opencvsecurity.models.frame_model import FrameModel

class Camera(ABC):

    options: FrameModel
    name: str
    stream: cv2.VideoCapture
    source: int

    thread = threading.Thread
    stopEvent = threading.Event

    def __init__(self, source, options):
        super().__init__()
        self.source = source
        self.options = options
        self.name = 'stream-{}'.format(source)
        self.stream = None
        self.thread = None
        self.stopEvent = None

    def __init_cam(self) -> None:
        if self.stream and self.stream.isOpened():
            return
        self.stream = cv2.VideoCapture(self.source)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.options.video_format.video_format))

        width  = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if width > self.options.frame_width or height > self.options.frame_height:
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.options.frame_width)
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.options.frame_height)
        
        fps = self.stream.get(cv2.CAP_PROP_FPS)
        if fps > self.options.frame_fps:
            self.stream.set(cv2.CAP_PROP_FPS, self.options.frame_fps)

    def init_main(self) -> None:
        print('[INFO][{}] starting ...'.format(self.name))

        self.__init_cam()

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

    def read(self) -> tuple[bool, cv2.typing.MatLike]:
        if not self.stream.isOpened():
            raise NameError('Error reading frame')
        grabbed, frame = self.stream.read()
        return (grabbed, frame)

    def stop(self) -> None:
        try:
            print('[INFO][{}] closing ...'.format(self.name))
            self.stopEvent.set()
            time.sleep(1)
            self.release()
        except Exception as e:
            print(e)
            self.release()

    def release(self) -> None:
        if self.stream:
            self.stream.release()

    @abstractmethod
    def video_loop(self) -> None:
        raise NotImplementedError("Can't use 'set' on an ADC!")