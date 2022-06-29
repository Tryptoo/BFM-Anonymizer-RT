import cv2
import time
import numpy
from detection import detectFaces
import matplotlib.pyplot as plt
from constants import *
from FaceBlurring import Blurring, BlurringCV

def TreatCoords(face, imageShape):
    left = int(face[0] - face[2] * FACE_RECT_INCREASE_RATIO[0] / 2 + FACE_RECT_OFFSET[0])
    top = int(face[1] - face[3] * FACE_RECT_INCREASE_RATIO[1] / 2 + FACE_RECT_OFFSET[1])
    right = int(left + face[2] + face[2] * FACE_RECT_INCREASE_RATIO[0] + FACE_RECT_OFFSET[0])
    bottom = int(top + face[3] + face[3] * FACE_RECT_INCREASE_RATIO[1] + FACE_RECT_OFFSET[1])
    if left < 0:
        left = 0
    if top < 0:
        top = 0
    if right >= imageShape[1]:
        right = imageShape[1]-1
    if bottom >= imageShape[0]:
        bottom = imageShape[0]-1
    return (left, top, right, bottom)

def GetCenter(rect):
    return (rect[0] + (rect[2] - rect[0]) / 2, rect[1] + (rect[3] - rect[1]) / 2)

def ReplaceFaceRect(rect, diff, imageShape):
    rect = (rect[0] + diff[0], rect[1] + diff[1], rect[2] + diff[0], rect[3] + diff[1])
    if rect[0] < 0:
        rect = (0, rect[1], rect[2], rect[3])
    if rect[1] < 0:
        rect = (rect[0], 0, rect[2], rect[3])
    if rect[2] >= imageShape[1]:
        rect = (rect[0], rect[1], imageShape[1]-1, rect[3])
    if rect[3] >= imageShape[0]:
        rect = (rect[0], rect[1], rect[2], imageShape[0]-1)
    return rect

def AssembleImage(image, faces):
    for face in faces:
        rect = face["rect"]
        image[rect[1]:rect[1]+face["treatedRect"].shape[0], rect[0]:rect[0]+face["treatedRect"].shape[1]] = face["treatedRect"]
    return image

vid = cv2.VideoCapture(0)
lastTime = time.time()
treatedRects = []

while(True):
    # Capture the video frame by frame
    _, frame = vid.read()

    # Get faces coords
    facesCoords = detectFaces(frame, (MIN_FACE_RECT_SIZE, MAX_FACE_RECT_SIZE))

    i = 0
    while i < len(treatedRects):
        rect = treatedRects[i]
        rect["timeLeft"] -= (time.time() - lastTime)
        rect["updateTimeLeft"] -= (time.time() - lastTime)
        if rect["timeLeft"] <= 0:
            treatedRects.remove(rect)
            continue
        i += 1
    
    for face in facesCoords:
        skip = False
        face = TreatCoords(face, frame.shape)
        faceCenter = GetCenter(face)
        # cv2.rectangle(frame, 
        #    (int(faceCenter[0] - FACE_RECOGNITION_DISTANCE / 2), int(faceCenter[1] - FACE_RECOGNITION_DISTANCE / 2)),
        #    (int(faceCenter[0] + FACE_RECOGNITION_DISTANCE / 2), int(faceCenter[1] + FACE_RECOGNITION_DISTANCE / 2)),
        #    (0, 0, 0))

        for rect in treatedRects:
            rectCenter = GetCenter(rect["rect"])
            diff = (int(faceCenter[0] - rectCenter[0]), int(faceCenter[1] - rectCenter[1]))
            if abs(diff[0]) <= FACE_RECOGNITION_DISTANCE and abs(diff[1]) <= FACE_RECOGNITION_DISTANCE:
                skip = True
                if rect["updateTimeLeft"] > 0:
                    rect["rect"] = ReplaceFaceRect(rect["rect"], diff, frame.shape)
                else:
                    rect["rect"] = face
                rect["timeLeft"] = RECT_DELETE_DELAY
                break
        if not skip:
            treatedRects.append({ "rect" : face , "timeLeft" : RECT_DELETE_DELAY, "updateTimeLeft" : 0 })
    

    # Apply blur
    for rect in treatedRects:
        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        if rect["updateTimeLeft"] <= 0:
            if BLUR_WITH_CV2 :
                rect["treatedRect"] = BlurringCV(frame, rect["rect"], BLUR_FACTOR)
            else :
                rect["treatedRect"] = Blurring(frame, rect["rect"], BLUR_FACTOR)
            rect["updateTimeLeft"] = BLUR_UPDATE_DELAY

    frame = AssembleImage(frame, treatedRects)

    # FPS Counter
    fps = str(int(10 / (time.time() - lastTime)) / 10) + " fps"
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