from flask import Flask, request, render_template
#from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
socketio = SocketIO(app, cors_allowed_origins="*")
#CORS(app)

users = {}
@socketio.on('disconnect')
def on_disconnect():
    users.pop(request.sid, 'No user found')
    socketio.emit('message', users)
    print("User disconnected!\nThe users are: ", users)

@socketio.on('connect')
def on_connect(methods=['GET', 'POST']):
    user_name = request.args.get('user_name') # /a?user_name=example
    users[request.sid] = user_name
    socketio.emit('message', users)
    print("New user sign in!\nThe users are: ", users)
    
    

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
    socketio.run(app, port=9090, debug=True)

if __name__ == '__main__':
    socketio.run(app, port=9090, debug=True)