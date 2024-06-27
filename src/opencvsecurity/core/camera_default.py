#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from src.opencvsecurity.core.definitions.camera import Camera, cv2
import tkinter as tk
from PIL import ImageTk, Image
import datetime
import os
import pathlib
import imutils
import threading

class CameraDefault(Camera):

    def __init__(self, source=0):
        super().__init__(source=source)
        self.outputPath = str(pathlib.Path(__file__).parent.resolve())
        self.frame = None
        self.thread = None
        self.stopEvent = None

    def init(self) -> None:

        self.init_now()

        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.panel = None

        btn = tk.Button(self.root, text='Snapshot!', command=self.takeSnapshot)
        btn.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        self.root.wm_title('Title')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.onClose)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        
        self.root.mainloop()

        #vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        #vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        #vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        #vid.set(cv2.CAP_PROP_FPS, 120)

        #self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        #self.stream.set(cv2.CAP_PROP_FPS, 30)
        #self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #out1 = cv2.VideoWriter('output1.avi', fourcc, 20.0, (640,480))
        # inside the loop
        #if grabbed:
            #out1.write(frame)
        
    def takeSnapshot(self):
        ts = datetime.datetime.now()
        file_name = '{}.jpg'.format(ts.strftime('%Y-%m-%d_%H-%M-%S'))
        p = os.path.sep.join((self.outputPath, file_name))
        # save the file
        cv2.imwrite(p, self.frame.copy())
        print('[INFO] saved {}'.format(file_name))

    def onClose(self):
        print('[INFO] closing ...')
        self.stopEvent.set()
        self.stop()
        self.root.quit()

    def videoLoop(self) -> None:
        try:
            while not self.stopEvent.is_set():
                grabbed, self.frame = self.read()
                if grabbed:
                    self.frame = imutils.resize(self.frame, width=300)
                    
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
                    image = Image.fromarray(image)
                    image = ImageTk.PhotoImage(image=image)

                    if self.panel is None:
                        self.panel = tk.Label(image=image)
                        self.panel.image = image
                        self.panel.pack(side='left', padx=10, pady=10)
                    else:
                        self.panel.configure(image=image)
                        self.panel.image = image
                else:
                    break
        except RuntimeError as e:
            print('[ERROR] error', e)