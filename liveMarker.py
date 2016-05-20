from marker import marker
import numpy as np
import cv2

if __name__ == "__main__":
    # external camera
    import sys
    if len(sys.argv)>1:
        print sys.argv
        cap = cv2.VideoCapture(sys.argv[1])
        count_frames = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            result = marker().find(frame, debug = 0, show = 0)
            if len(result) > 0:
                print result
                cv2.imshow("frame", marker().find(frame, debug = 0, show =1))
                cv2.waitKey(0)
            count_frames += 1
            frame_size = frame.shape[:2]
        print "frames amount:", count_frames
        print "frames size:", frame_size
        print "fps:", cap.get(cv2.CAP_PROP_FPS)
    else:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = marker().find(frame,debug = 0, show = 0)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
