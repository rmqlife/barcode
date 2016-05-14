from marker import marker
import numpy as np
import cv2

if __name__ == "__main__":
    # external camera
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        frame = marker().find(frame,debug = 0, show = 1)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if not ret:
            break
    cap.release()
    cv2.destroyAllWindows()
