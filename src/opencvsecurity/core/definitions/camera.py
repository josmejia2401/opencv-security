#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import cv2
from abc import ABC, abstractmethod
import threading
import time

from src.opencvsecurity.models.frame_model import FrameModel

class Camera(ABC):

    _options: FrameModel
    _name: str
    _stream: cv2.VideoCapture
    _source: int

    _frame = cv2.typing.MatLike
    _thread = threading.Thread
    _stopEvent = threading.Event

    def __init__(self, source, options):
        super().__init__()
        self._source = source
        self._options = options
        self._name = 'stream-{}'.format(source)
        self._stream = None

        self._frame = None
        self._thread = None
        self._stopEvent = None

    def __init_cam(self) -> None:
        if self._stream and self._stream.isOpened():
            return
        self._stream = cv2.VideoCapture(self._source)
        self._stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self._options.video_format.video_format))
        self._stream.set(cv2.CAP_PROP_FRAME_WIDTH, self._options.video_format.video_width)
        self._stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self._options.video_format.video_height)
        self._stream.set(cv2.CAP_PROP_FPS, self._options.frame_fps)

    def init_main(self) -> None:
        print('[INFO][{}] starting ...'.format(self._name))

        self.__init_cam()

        self._stopEvent = threading.Event()
        self._thread = threading.Thread(target=self.video_loop, args=())
        self._thread.start()

    def read(self) -> tuple[bool, cv2.typing.MatLike]:
        if not self._stream.isOpened():
            raise NameError('Error reading frame')
        grabbed, frame = self._stream.read()
        return (grabbed, frame)

    def stop(self) -> None:
        try:
            print('[INFO][{}] closing ...'.format(self._name))
            self._stopEvent.set()
            time.sleep(1)
            self.release()
        except Exception as e:
            print(e)
            self.release()

    def release(self) -> None:
        if self._stream:
            self._stream.release()

    @abstractmethod
    def video_loop(self) -> None:
        raise NotImplementedError("Can't use 'set' on an ADC!")