from src.core.sub.sub_worker import SubWorker
from src.core.models.proccess_frame_model import ProcessFrameModel
from src.core.camera_async import CameraAsync
from src.webapp.manage_user import ManageUser

import base64
import cv2
from flask_socketio import SocketIO


class ManageFrame(SubWorker):

    socketio: SocketIO
    _camera_async: CameraAsync
    _manage_user: ManageUser
    _selected_cam: int
    _selected_dim: str

    def __init__(self, socketio: SocketIO):
        super().__init__()
        self.socketio = socketio
        self._camera_async = CameraAsync()
        self._manage_user = ManageUser()

    def init(self):
        self.camera_async.init()
        self.camera_async.frame_worker.attach(clazz=self)
        self.camera_async.start()
        self.selected_cam = 0
        self.selected_dim = '640x480'

    def stop(self):
        self.camera_async.on_close()

    def on_message(self, message: ProcessFrameModel) -> None:
        if self.manage_user.size() > 0 and message.frame is not None and message.source == self.selected_cam:
            try:
                width = 480
                heigth = 320
                if self.selected_dim:
                    width = int(self.selected_dim.split("x")[0])
                    heigth = int(self.selected_dim.split("x")[1])
                
                frame = cv2.resize(message.frame, (width,heigth))
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                a_dict = {'frame': jpg_as_text, 'source': message.source}
                self.socketio.emit('message', a_dict)
            except Exception as e:
                print("[ERROR]", e)

    @property
    def camera_async(self):
        return self._camera_async
    
    @property
    def manage_user(self):
        return self._manage_user
    
    @property
    def selected_cam(self):
        return self._selected_cam
    
    @selected_cam.setter
    def selected_cam(self, selected_cam):
        self._selected_cam = selected_cam

    @property
    def selected_dim(self):
        return self._selected_dim
    
    @selected_dim.setter
    def selected_dim(self, selected_dim):
        self._selected_dim = selected_dim