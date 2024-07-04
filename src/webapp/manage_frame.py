from src.core.sub.sub_worker import SubWorker
from src.core.models.proccess_frame_model import ProcessFrameModel
from src.core.camera_async import CameraAsync
from src.webapp.manage_user import ManageUser
from src.core.models.subscriber_model import SubscriberModel

import base64
import cv2
from flask_socketio import SocketIO


class ManageFrame(SubWorker):

    socketio: SocketIO
    _camera_async: CameraAsync
    _manage_user: ManageUser

    def __init__(self, socketio: SocketIO):
        super().__init__()
        self.socketio = socketio
        self._camera_async = CameraAsync()
        self._manage_user = ManageUser()

    def init(self):
        self.camera_async.init()
        attach = SubscriberModel(
            clazz=self,
            name='ManageFrame',
            topic='ALL',
        )
        self.camera_async.start()
        self.camera_async.frame_worker.attach(attach)

    def stop(self):
        self.camera_async.on_close()

    def on_message(self, message: ProcessFrameModel) -> None:
        if self.manage_user.size() > 0 and message.frame is not None:
            try:
                _, buffer = cv2.imencode('.jpg', message.frame)
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