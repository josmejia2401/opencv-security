#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.webapp.models.config_user_model import ConfigUserModel

class ManageUser:
    users: dict[str, ConfigUserModel]
    
    def __init__(self) -> None:
        self.users = {}


    def add_user(self, username: str, sid = str):
        if username in self.users:
            if self.users[username].sid is None:
                self.users[username].sid = []
            if sid not in self.users[username].sid:
                self.users[username].sid.append(sid)
        else:
            sid_list = []
            sid_list.append(sid)
            self.users[username] = ConfigUserModel(
                dimension='320x240',
                sid=sid_list,
                source=0,
                username=username
            )    
    
    def remove_user(self, username):
        if username in self.users:
            del self.users[username]

    def remove_session(self, sid):
        for user in self.users:
            if sid in user.sid:
                del user.sid[sid]

    def clear(self):
        self.users = {}

    def size(self):
        return len(self.users)
    
    def get_session_from_user(self, username):
        if username in self.users and len(self.users[username].sid) > 0:
            return self.users[username].sid[0]
        return None
    
    def add_source(self, username, source):
        if username in self.users:
            self.users[username].source = source
            print('[INFO] add_source', username, source)

    def add_dimension(self, username, dimension):
        if username in self.users:
            self.users[username].dimension = dimension
            print('[INFO] add_dimension', username, dimension)
