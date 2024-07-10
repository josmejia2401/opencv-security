#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import queue
import threading

from src.core.models.proccess_frame_model import ProcessFrameModel
from src.core.models.frame_model import FrameModel
from src.core.camera_default import CameraDefault
from src.core.cam_list import cam_list
from src.core.models.video_format_model import VideoFormatModel
from src.core.workers.frame_worker import FrameWorker
from src.core.utils.utils import build_home_directory

class CameraAsync(threading.Thread):
    
    _frame_worker: FrameWorker
    _q: queue.Queue
    options: FrameModel
    cameras_attach: list[type[CameraDefault]]
    cameras_available: list[type[int]]
    screen_width: int
    screen_height: int
    stopEvent: threading.Event

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._q = queue.Queue()
        self.cameras_available = []
        self.stopEvent = threading.Event()
        self.camera_default = None
        self.screen_width = None
        self.screen_height = None
        self._frame_worker = None
        self.options = None
        self.cameras_attach = []
        self.cameras_available = cam_list()

    def init(self) -> None:
        self.init_options()
        self.init_camera()
        self.init_workers()

    def init_workers(self):
        self.frame_worker = FrameWorker(q=self.q, options=self.options)
        self.frame_worker.start()

    def init_options(self) -> None:
        #320x240, 640x480, 800x480, 1024x600, 1024x768, 1440x900, 1920x1200, 1280x720, 1920x1080, 768x576, 720x480
        self.options = FrameModel(
            frame_width=1280,
            frame_height=720,
            frame_fps=10, #30, 60, 120
            video_format=VideoFormatModel(
                #output_path=str(pathlib.Path(__file__).parent.resolve()),
                output_path=build_home_directory(),
                video_format='mp4v',
                video_height=480,
                video_width=720,
                video_color=True
            )
        )

    def init_camera(self):
        for source in self.cameras_available:
            camera_default = CameraDefault(
                source=source,
                options=self.options,
                q=self.q
            )
            self.cameras_attach.append(camera_default)
        
    def run(self):
        while not self.stopEvent.is_set():
            try:
                # inicia las camaras atadas
                for cam in self.cameras_attach:
                    cam.init()
                self.stopEvent.wait()
            except Exception as e:
                print('[ERROR] Exception', e)

    def on_close(self):
        print('[INFO] closing camera async...')
        self.stopEvent.set()
        self.frame_worker.on_close()
        for cam in self.cameras_attach:
            cam.on_close()

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

    @property
    def frame_worker(self):
        return self._frame_worker

    @frame_worker.setter
    def frame_worker(self, frame_worker):
        self._frame_worker = frame_worker

    @property
    def q(self):
        return self._q