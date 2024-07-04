from flask import Flask, request, render_template
from flask_cors import CORS#, cross_origin
from flask_socketio import SocketIO
import json
from src.webapp.manage_frame import ManageFrame
from src.webapp.models.user_model import UserModel

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

manage_frame = ManageFrame(socketio=socketio)

@socketio.on('disconnect')
def on_disconnect():
    username = request.args.get('username') # /a?username=example
    if not username:
        manage_frame.manage_user.remove_session(sid=request.sid)
    else:
        manage_frame.manage_user.remove_user(username=username)
    socketio.emit('message', { "message": "OK", "username": username, "sid": request.sid})
    print("User disconnected!\nThe users are: ", username)

@socketio.on('connect')
def on_connect(methods=['GET', 'POST']):
    username = request.args.get('username') # /a?username=example
    fullname = request.args.get('fullname') # /a?fullname=example
    user = UserModel(
        full_name=fullname,
        username=username,
        sid=request.sid
    )
    manage_frame.manage_user.add_user(user, request.sid)
    print("New user sign in!\nThe users are: ", username)


@socketio.on('message')
def on_message(message, methods=['GET', 'POST']):
    print('received message: ' + str(message))
    message['from'] = request.sid
    socketio.emit('message', message, room=request.sid)
    socketio.emit('message', message, room=message['to'])

@app.route('/')
def index():
    return render_template('index.html')

def main():
    manage_frame.init()

def stop():
    manage_frame.stop()

if __name__ == '__main__':
    manage_frame.init()
    socketio.run(app, port=9090, debug=True)