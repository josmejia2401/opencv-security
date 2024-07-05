from src.webapp.server import app, main, socketio, stop


if __name__ == '__main__':
    try:
        main()
        socketio.run(app, host='0.0.0.0', port=9090, debug=True)
    except KeyboardInterrupt as e:
        stop()