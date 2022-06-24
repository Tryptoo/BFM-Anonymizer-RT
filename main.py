import cv2
import time
from detection import detectFaces
from constants import *
from FaceBlurring import Blurring

vid = cv2.VideoCapture(0)
lastTime = time.time()
oldfaces = []

while(True):
    # Capture the video frame by frame
    _, frame = vid.read()

    # Get faces coords
    facesCoords = detectFaces(frame, (MIN_FACE_RECT_SIZE, MAX_FACE_RECT_SIZE))
    filtered_img = frame
    if(len(facesCoords) <= 0):
        facesCoords = oldfaces
    else :
        oldfaces = facesCoords
    for face in facesCoords:
        left = int(face[0] - face[2] * FACE_RECT_INCREASE_RATIO[0] / 2 + FACE_RECT_OFFSET[0])
        top = int(face[1] - face[3] * FACE_RECT_INCREASE_RATIO[1] / 2 + FACE_RECT_OFFSET[1])
        right = int(left + face[2] + face[2] * FACE_RECT_INCREASE_RATIO[0] + FACE_RECT_OFFSET[0])
        bottom = int(top + face[3] + face[3] * FACE_RECT_INCREASE_RATIO[1] + FACE_RECT_OFFSET[1])
        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        filtered_img = Blurring(filtered_img, (left, top, right, bottom), BLUR_FACTOR)

    # FPS Counter
    fps = str(int(1 * 10 / (time.time() - lastTime)) / 10) + " fps"
    lastTime = time.time()
    cv2.putText(filtered_img, fps, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 0), 2, 2)
   
    # Display the resulting frame
    cv2.imshow('frame', filtered_img)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()