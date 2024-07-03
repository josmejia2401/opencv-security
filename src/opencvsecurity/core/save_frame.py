import cv2
from src.opencvsecurity.models.frame_model import FrameModel
from datetime import datetime
from os import path, rename
from pathlib import Path
import imutils

class SaveFrame:
    out: cv2.VideoWriter
    options: FrameModel
    source: int
    source_name: str
    current_day: str
    current_time: str

    def __init__(self, options, source) -> None:
        self.out = None
        self.options = options
        self.source = source
        self.source_name = 'stream-{}'.format(source)
        self.current_day = None
        self.current_time = None
        self.init()

    
    def init(self):
        self.create_stream()
        self.check_day_changed()
        self.check_hour_changed()
        p = self.get_file_name_video()
        if  Path(p).is_file():
            try:
                fourcc = cv2.VideoWriter_fourcc(*self.options.video_format.video_format)
                self.out = cv2.VideoWriter(filename=p,
                                            fourcc=fourcc,
                                            fps=self.options.frame_fps,
                                            frameSize=(self.options.video_format.video_width, self.options.video_format.video_height),
                                            isColor=self.options.video_format.video_color)
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
        p = path.sep.join((self.options.video_format.output_path, self.source_name))
        Path(str(p)).mkdir(parents=True, exist_ok=True)


    def check_day_changed(self) -> bool:
        ts = datetime.now()
        
        current_day_temp = ts.strftime('%Y-%m-%d')
        p = path.sep.join((self.options.video_format.output_path, self.source_name, current_day_temp))
        Path(str(p)).mkdir(parents=True, exist_ok=True)

        if self.current_day is None:
            self.current_day = current_day_temp
            return True
        
        if self.current_day != current_day_temp:
            self.current_day = current_day_temp
            return True
        
        return False

    def check_hour_changed(self) -> bool:
        ts = datetime.now()
        current_time_temp = ts.strftime('%H')

        if self.current_time is None:
            self.current_time = current_time_temp
            return True
        
        if self.current_time != current_time_temp:
            self.current_time = current_time_temp
            return True
        
        return False

    
    def get_file_name_video(self):
        p = path.sep.join((
            self.options.video_format.output_path,
            self.source_name,
            self.current_day,
            self.current_time
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
        if self.out is None:
            fourcc = cv2.VideoWriter_fourcc(*self.options.video_format.video_format)
            self.out = cv2.VideoWriter(filename=p,
                                        fourcc=fourcc,
                                        fps=self.options.frame_fps,
                                        #frameSize=(self.options.frame_width, self.options.frame_height),
                                        frameSize=(self.options.video_format.video_width, self.options.video_format.video_height),
                                        isColor=self.options.video_format.video_color)
        if grabbed == True:
            frame = self.resize(
                frame=frame,
                width=self.options.video_format.video_width,
                height=self.options.video_format.video_height
            )
            self.out.write(frame)

    def save_image(self, grabbed: bool, frame: cv2.typing.MatLike):
        ts = datetime.now()
        file_name = '{}.jpg'.format(ts.strftime('%Y-%m-%d_%H-%M-%S'))
        p = path.sep.join((self.options.video_format.output_path, str(self.source_name)))
        p = path.sep.join((p, file_name))
        # save the file
        if grabbed == True:
            cv2.imwrite(p, frame.copy())
        print('[INFO] saved {}'.format(file_name))

    def release(self) -> None:
        if self.out:
            print('[INFO] saved {}'.format(self.get_file_name_video()))
            self.out.release()
            self.out = None

    def resize(self, frame, width, height) -> any:
        try:
            if frame is None:
                return None
            return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        except Exception as e:
            return imutils.resize(frame, width, height)
