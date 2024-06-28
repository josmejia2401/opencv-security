import cv2
from src.opencvsecurity.models.frame_model import FrameModel
from datetime import datetime
from os import path

class SaveFrame:
    _out: cv2.VideoWriter
    _options: FrameModel
    _source: int

    def __init__(self, options, source) -> None:
        self._out = None
        self._options = options
        self._source = source

    def save_video(self, grabbed: bool, frame: cv2.typing.MatLike) -> None:
        # save video config
        ts = datetime.now()
        file_name = '{}.mp4'.format(ts.strftime('%Y-%m-%d_%H-%M-%S'))
        p = path.sep.join((self._options.output_path, str(self._source)))
        p = path.sep.join((p, file_name))
        # save the file
        if self._out is None:
            fourcc = cv2.VideoWriter_fourcc(*self._options.video_format)
            self._out = cv2.VideoWriter(p, fourcc, 20.0, (self._options.frame_width, self._options.frame_height))
        if grabbed == True:
             self._out.write(frame)
        print('[INFO] saved {}'.format(file_name))

    def save_image(self, grabbed: bool, frame: cv2.typing.MatLike):
        ts = datetime.now()
        file_name = '{}.jpg'.format(ts.strftime('%Y-%m-%d_%H-%M-%S'))
        p = path.sep.join((self._options.output_path, str(self._source)))
        p = path.sep.join((p, file_name))        # save the file
        if grabbed == True:
            cv2.imwrite(p, frame.copy())
        print('[INFO] saved {}'.format(file_name))

    def release(self) -> None:
        if self._out:
            self._out.release()