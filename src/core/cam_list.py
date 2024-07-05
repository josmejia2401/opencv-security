# camlist.py
# Lists all avaiable cameras attached to the computer
import cv2
import sys

def cam_list() -> list[type[int]]:
    print(f"OpenCV version: {cv2.__version__} - Python {sys.version}")
    max_cameras = 1
    avaiable = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        _, frame = cap.read()
        if frame is None:
            print(f"Camera index {i:02d} not found...")
            continue
        avaiable.append(i)
        cap.release()
        print(f"Camera index {i:02d} OK!")
    print(f"Cameras found: {avaiable}")
    return avaiable