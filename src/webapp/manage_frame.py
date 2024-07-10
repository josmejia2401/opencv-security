#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.core.sub.sub_worker import SubWorker
from src.core.models.proccess_frame_model import ProcessFrameModel
from src.core.camera_async import CameraAsync
from src.webapp.manage_user import ManageUser
from src.webapp.models.config_user_model import ConfigUserModel

import base64
import cv2
from flask_socketio import SocketIO
import zlib


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
        self.camera_async.frame_worker.attach(clazz=self)
        self.camera_async.start()

    def stop(self):
        self.camera_async.on_close()

    def on_message(self, message: ProcessFrameModel) -> None:
        if self.manage_user.size() > 0 and message.frame is not None:
            for user_connected in self.manage_user.users:
                user = self.manage_user.users[user_connected]
                self.process_frame(user=user,message=message)

    def process_frame(self, user: ConfigUserModel, message: ProcessFrameModel):
        try:
            if message.source != user.source or len(user.sid) == 0:
                return
            width = int(user.dimension.split("x")[0])
            heigth = int(user.dimension.split("x")[1])
            frame = cv2.resize(message.frame, (width,heigth))
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            jpg_as_text = zlib.compress(jpg_as_text)
            #a_dict = {'frame': jpg_as_text, 'source': message.source}
            #self.socketio.emit('frame', a_dict, to=sid, room=sid)
            for sid in user.sid:
                self.socketio.emit('frame', jpg_as_text, to=sid, room=sid)
        except Exception as e:
            print("[ERROR]", e)

    @property
    def camera_async(self):
        return self._camera_async
    
    @property
    def manage_user(self):
        return self._manage_user
    
    @manage_user.setter
    def manage_user(self, manage_user):
        self._manage_user = manage_user