from src.webapp.server import app, main, socketio, stop


if __name__ == '__main__':
    try:
        main()
        socketio.run(app, port=9090, debug=True)
    except KeyboardInterrupt as e:
        stop()