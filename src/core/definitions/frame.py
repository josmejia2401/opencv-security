#!/usr/bin/env python3
#!/usr/bin/python3.8
# OpenCV 4.2, Raspberry pi 3/3b/4b - test on macOS
import cv2

class Frame:
    
    @staticmethod
    def frame_diff(frame1, frame2):
        # Difference between frame1(image) and frame2(image)
        diff = cv2.absdiff(frame1, frame2)
        # Converting color image to gray_scale image
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # Converting gray scale image to GaussianBlur, so that change can be find easily
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # If pixel value is greater than 20, it is assigned white(255) otherwise black
        grabbed, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        return grabbed, thresh

    @staticmethod
    def contours(frame1, frame2):
        # Difference between frame1(image) and frame2(image)
        diff = cv2.absdiff(frame1, frame2)
        # Converting color image to gray_scale image
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # Converting gray scale image to GaussianBlur, so that change can be find easily
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # If pixel value is greater than 20, it is assigned white(255) otherwise black
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=4)
        # finding contours of moving object
        contours, hirarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hirarchy
    
    @staticmethod
    def frame_mov(frame1, frame2):
        contours, _ = Frame.contours(frame1, frame2)
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            referenceArea = Frame.is_object(contour)
            if referenceArea is None:
                continue
            Frame.draw(frame1, x, y, w, h, "movimiento")
        return True, frame1

    @staticmethod
    def draw(frame, x, y, w, h, text):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(frame, text, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    @staticmethod
    def is_object(contour):
        referenceArea = cv2.contourArea(contour)
        if referenceArea < 50:
            return None
        return referenceArea
    
    