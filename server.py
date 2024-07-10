#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.webapp.server import app, main, socketio, stop

if __name__ == '__main__':
    try:
        main()
        socketio.run(app, host='0.0.0.0', port=9090, debug=True, use_reloader=False)
    except KeyboardInterrupt as e:
        print('KeyboardInterrupt...')
        stop()
    except Exception as e:
        print('Exception...')
        stop()
    except RuntimeError as e:
        print('Exception...')
        stop()
    finally:
        stop()