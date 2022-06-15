import cv2
import time
from detection import detectFaces
from constants import *

vid = cv2.VideoCapture(0)
lastTime = time.time()

while(True):
    # Capture the video frame by frame
    _, frame = vid.read()

    facesCoords = detectFaces(frame, (MIN_FACE_RECT_SIZE, MAX_FACE_RECT_SIZE))

    for face in facesCoords:
        cv2.rectangle(frame, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (0, 0, 255), 2)

    # FPS Counter
    fps = str(int(1 * 10 / (time.time() - lastTime)) / 10) + " fps"
    lastTime = time.time()
    cv2.putText(frame, fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 0), 2, 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()