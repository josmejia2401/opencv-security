
class ManageUser:

    users: dict[str, list[str]]
    
    def __init__(self) -> None:
        self.users = {}

    def add_user(self, username: str, sid = str):
        if username in self.users:
            if sid not in self.users[username]:
                self.users[username].append(sid)
        else:
            sid = []
            sid.append(sid)
            self.users[username] = sid        
    
    def remove_user(self, username):
        if username in self.users:
            del self.users[username]

    def remove_session(self, sid):
        for user in self.users:
            if sid in user:
                del user[sid]

    def clear(self):
        self.users = {}

    def size(self):
        return len(self.users)