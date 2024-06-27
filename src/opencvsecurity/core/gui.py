#!/usr/bin/env python3
#!/usr/bin/python3.12.4
import cv2
import tkinter as tk
from src.opencvsecurity.core.save_frame import SaveFrame
from PIL import ImageTk, Image

class Gui:

    root: tk.Tk
    panel: tk.Label
    save_frame: SaveFrame
    frame: cv2.typing.MatLike
    callback: any


    def __init__(self, save_frame):
        super().__init__()
        self.root = None
        self.panel = None
        self.save_frame = save_frame
        self.frame = None
        self.callback = None

    def init(self, callback) -> None:
        self.callback = callback

        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.panel = None

        btn = tk.Button(self.root, text='Snapshot!', command=self.take_snapshot)
        btn.pack(side='bottom', fill='both', expand='yes', padx=10, pady=10)

        self.root.wm_title('Title')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)
        
        self.root.mainloop()
        
    
    def take_snapshot(self):
        self.save_frame.save_image(True, self.frame)
   
    def on_close(self):
        print('[INFO] closing ...')
        self.callback()
        self.root.quit()

    def draw_frame(self, frame: cv2.typing.MatLike) -> None:
        try:
            self.frame = frame
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
        except RuntimeError as e:
            print('[ERROR] error', e)