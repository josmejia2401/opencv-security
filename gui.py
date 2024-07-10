#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.gui.kernel import Kernel

if __name__ == '__main__':
    k = Kernel()
    try:
        k.init()
    except KeyboardInterrupt as e:
        print('KeyboardInterrupt...')
        k.on_close()
    except Exception as e:
        print('Exception...')
        k.on_close()
    except RuntimeError as e:
        print('Exception...')
        k.on_close()
    finally:
        k.on_close()
