from src.webapp.models.user_model import UserModel

class ManageUser:

    _username_allowed: list[str]
    users: dict[str, UserModel]
    
    def __init__(self) -> None:
        self.users = {}
        self._username_allowed = []
        self.username_allowed.append('josem')
        self.username_allowed.append('esterc')

    def add_user(self, data: UserModel, sid = str):
        if data.username not in self.username_allowed:
            raise Exception('Username not allowed')

        if data.username in self.users:
            if sid not in self.users[data.username].sid:
                self.users[data.username].sid.append(sid)
        else:
            data.sid = []
            data.sid.append(sid)
            self.users[data.username] = data
        
        print("<<<<<<<<", self.users[data.username])
    
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

    @property
    def username_allowed(self):
        return self._username_allowed