import cv2
from src.opencvsecurity.models.frame_model import FrameModel
from datetime import datetime
from os import path, rename
from pathlib import Path

class SaveFrame:
    _out: cv2.VideoWriter
    _options: FrameModel
    _source: str
    _current_day: str
    _current_time: str

    def __init__(self, options, source) -> None:
        self._out = None
        self._options = options
        self._source = 'stream-{}'.format(source)
        self._current_day = None
        self._current_time = None
        self.init()

    
    def init(self):
        self.create_stream()
        self.check_day_changed()
        self.check_hour_changed()
        p = self.get_file_name_video()
        if  Path(p).is_file():
            try:
                fourcc = cv2.VideoWriter_fourcc(*self._options.video_format.video_format)
                self._out = cv2.VideoWriter(filename=p,
                                            fourcc=fourcc,
                                            fps=self._options.frame_fps,
                                            frameSize=(self._options.video_format.video_width, self._options.video_format.video_height),
                                            isColor=self._options.video_format.video_color)
                self.release()
                self.rename_video(p)
            except Exception as ex:
                print('[ERROR] init', ex)
                self.rename_video(p)
        
    def rename_video(self, p):
        ts = datetime.now()
        current_time_temp = ts.strftime('%H-%M-%S')
        new_p = p.replace('.mp4', '-{}.mp4'.format(current_time_temp))
        rename(p, new_p)
        

    """
    /stream-{index}/yyyy-mm-dd/hh.{ext}
    """
    def create_stream(self):
        p = path.sep.join((self._options.video_format.output_path, self._source))
        Path(str(p)).mkdir(parents=True, exist_ok=True)


    def check_day_changed(self) -> bool:
        ts = datetime.now()
        
        current_day_temp = ts.strftime('%Y-%m-%d')
        p = path.sep.join((self._options.video_format.output_path, self._source, current_day_temp))
        Path(str(p)).mkdir(parents=True, exist_ok=True)

        if self._current_day is None:
            self._current_day = current_day_temp
            return True
        
        if self._current_day != current_day_temp:
            self._current_day = current_day_temp
            return True
        
        return False

    def check_hour_changed(self) -> bool:
        ts = datetime.now()
        current_time_temp = ts.strftime('%H')

        if self._current_time is None:
            self._current_time = current_time_temp
            return True
        
        if self._current_time != current_time_temp:
            self._current_time = current_time_temp
            return True
        
        return False

    
    def get_file_name_video(self):
        p = path.sep.join((
            self._options.video_format.output_path,
            self._source,
            self._current_day,
            self._current_time
        ))
        return '{}.mp4'.format(str(p))

    def save_video(self, grabbed: bool, frame: cv2.typing.MatLike) -> None:

        self.create_stream()
        day_changed = self.check_day_changed()
        day_changed = self.check_hour_changed()

        if day_changed or day_changed:
            self.release()
        
        p = self.get_file_name_video()
        
        # save the file
        if self._out is None:
            fourcc = cv2.VideoWriter_fourcc(*self._options.video_format.video_format)
            self._out = cv2.VideoWriter(filename=p,
                                        fourcc=fourcc,
                                        fps=self._options.frame_fps,
                                        frameSize=(self._options.video_format.video_width, self._options.video_format.video_height),
                                        isColor=self._options.video_format.video_color)
        if grabbed == True:
             self._out.write(frame)

    def save_image(self, grabbed: bool, frame: cv2.typing.MatLike):
        ts = datetime.now()
        file_name = '{}.jpg'.format(ts.strftime('%Y-%m-%d_%H-%M-%S'))
        p = path.sep.join((self._options.video_format.output_path, str(self._source)))
        p = path.sep.join((p, file_name))
        # save the file
        if grabbed == True:
            cv2.imwrite(p, frame.copy())
        print('[INFO] saved {}'.format(file_name))

    def release(self) -> None:
        if self._out:
            print('[INFO] saved {}'.format(self.get_file_name_video()))
            self._out.release()
            self._out = None