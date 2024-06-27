#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import cv2

class Camera:

    def __init__(self, source=0):
        super().__init__()
        self.name = 'stream-{}'.format(source)
        self.source = source
        self.stream = None


    def init_now(self) -> None:
        if self.stream and self.stream.isOpened():
            return
        self.stream = cv2.VideoCapture(self.source)

    def read(self) -> tuple[bool, cv2.typing.MatLike]:
        (grabbed, frame) = self.stream.read()
        return (grabbed, frame)

    def stop(self) -> None:
        try:
            self.release()
        except Exception as e:
            print(e)
            self.release()

    def release(self) -> None:
        if self.stream:
            self.stream.release()