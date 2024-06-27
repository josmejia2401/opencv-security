#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import cv2
from abc import ABC, abstractmethod
from src.opencvsecurity.models.frame_model import FrameModel

class Camera(ABC):

    _options: FrameModel
    _name: str
    _stream: cv2.VideoCapture

    def __init__(self, options):
        super().__init__()
        self._options = options
        self._name = 'stream-{}'.format(self._options.source)
        self._stream = None

    def init_now(self) -> None:
        if self._stream and self._stream.isOpened():
            return
        self._stream = cv2.VideoCapture(self._options.source)
        self._stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self._options.video_format))
        self._stream.set(cv2.CAP_PROP_FRAME_WIDTH, self._options.frame_width)
        self._stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self._options.frame_height)
        self._stream.set(cv2.CAP_PROP_FPS, self._options.frame_fps)

    def read(self) -> tuple[bool, cv2.typing.MatLike]:
        grabbed, frame = self._stream.read()
        return (grabbed, frame)

    def stop(self) -> None:
        try:
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