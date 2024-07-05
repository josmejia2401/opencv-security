from flask import Flask, request, render_template, redirect, url_for, flash, session, Response
from flask_cors import CORS

import json

from flask_socketio import SocketIO
from src.webapp.manage_frame import ManageFrame
from src.webapp.db.manage_db import ManageDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
manage_db = ManageDB()
manage_frame = ManageFrame(socketio=socketio)

@socketio.on('disconnect')
def on_disconnect():
    username = request.args.get('username') # /a?username=example
    if not username:
        manage_frame.manage_user.remove_session(sid=request.sid)
    else:
        manage_frame.manage_user.remove_user(username=username)
        
    current_session = session._get_current_object()
    if current_session.get('logged_in', False) is False or current_session.get('username', 'Guest') != current_session:
        current_session['logged_in'] = False

    socketio.emit('message', { "message": "OK", "username": username, "sid": request.sid})
    print("User disconnected!\nThe users are: ", username)

@socketio.on('connect')
def on_connect(methods=['GET', 'POST']):
    username = request.args.get('username')
    current_session = session._get_current_object()
    if current_session.get('logged_in', False) is False or current_session.get('username', 'Guest') != username:
        current_session['logged_in'] = False

    if current_session.get('logged_in', False) is False:
        return
    manage_frame.manage_user.add_user(username, request.sid)
    print("========= New user sign in! =========\nThe users are: ", username)


@socketio.on('message')
def on_message(message, methods=['GET', 'POST']):
    print('received message: ' + str(message))
    message['from'] = request.sid
    socketio.emit('message', message, room=request.sid)
    socketio.emit('message', message, room=message['to'])

@app.route('/')
def index():
    current_session = session._get_current_object()
    if current_session.get('logged_in', False) is False:
        current_session['logged_in'] = False
    return render_template('index.html', current_session=current_session)

@app.route('/profile')
def profile():
    current_session = session._get_current_object()
    if current_session.get('logged_in', False) is False:
        current_session['logged_in'] = False
    return render_template('profile.html', current_session=current_session)

@app.route('/login')
def login():
    current_session = session._get_current_object()
    if current_session.get('logged_in', False) is False:
        current_session['logged_in'] = False
    return render_template('login.html', current_session=current_session)

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    users = manage_db.find_user_and_pass(username=username, password=password)

    current_session = session._get_current_object()

    if len(users) == 0:
        flash('Please check your login details and try again.')
        current_session['logged_in'] = False
        return redirect(url_for('login', current_session=current_session)) # if the user doesn't exist or password is wrong, reload the page
    
    current_session['username'] = username
    current_session['full_name'] = users[0][1]
    current_session['logged_in'] = True
    print('current_session.logged_in', current_session.get('logged_in', False) )

    return redirect(url_for('profile', current_session=current_session))

@app.route('/signup')
def signup():
    current_session = session._get_current_object()
    if current_session.get('logged_in', False) is False:
        current_session['logged_in'] = False
    return render_template('signup.html', current_session=current_session)

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    users = manage_db.find_user(username=username)

    current_session = session._get_current_object()

    if len(users) > 0:
        if current_session.get('logged_in', False) is False:
            current_session['logged_in'] = False
        flash('Email address already exists')
        return redirect(url_for('signup', current_session=current_session))
    manage_db.create_user(username, full_name, email, password)

    current_session['username'] = username
    current_session['full_name'] = full_name
    current_session['logged_in'] = True

    return redirect(url_for('login', current_session=current_session))

@app.route('/logout')
def logout():
    current_session = session._get_current_object()
    current_session['logged_in'] = False
    return redirect(url_for('index', current_session=current_session))

@app.route('/cameras_available')
def cameras_available():
    return manage_frame.camera_async.cameras_available

@app.route('/selected_cam')
def selected_cam():
    selected = request.args.get('selected') # /a?selected=0
    print('Cam selected', selected)
    manage_frame.selected_cam = int(selected)
    return Response(
    response='ok',
    status=200,
)

@app.route('/dimensions')
def dimensions():
    dimensions = ['320x240', '640x480', '800x480', '1024x600', '1024x768', '1440x900', '1920x1200', '1280x720', '1920x1080', '768x576', '720x480']
    return Response(
    response=json.dumps(dimensions),
    status=200,
    headers=dict({
        "content-type": "application/json"
    })
)

@app.route('/selected_dim')
def selected_selected_dimcam():
    selected = request.args.get('selected') # /a?selected=0
    print('Dim selected', selected)
    manage_frame.selected_dim = selected
    return Response(
    response='ok',
    status=200,
)

def main():
    manage_frame.init()
    manage_db.connect()
    manage_db.create_all()

def stop():
    manage_frame.stop()
    manage_db.close_connection()

if __name__ == '__main__':
    main()
    socketio.run(app, host='0.0.0.0', port=9090, debug=True, use_reloader=False)