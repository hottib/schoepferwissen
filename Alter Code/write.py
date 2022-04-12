from fileinput import filename
import cv2
from cv2 import VideoCapture
from matplotlib.image import pil_to_array
#from ffpyplayer.player import MediaPlayer

def main():
    windowsname = "Writing to a Video"
    cv2.namedWindow(windowsname)

    cap = cv2.VideoCapture('DATA/1.mp4')

    filename = "TESTOUT.avi"

    codec = cv2.VideoWriter_fourcc(*'XVID')
    framerate = 60
    resolution = (640,480)

    VideoOutPut = cv2.VideoWriter(filename, codec, framerate, resolution)

    if cap.isOpened():
        ret, frame = cap.read()
    else:
        rest = False
    
    while ret: 
        ret, frame = cap.read()

        VideoOutPut.write(frame)
        cv2.imshow(windowsname, frame)

        if cv2.waitKey(1)== 27:
            break

    cv2.destroyAllWindows()
    VideoOutPut.release()
    cap.release()
    # 

main()