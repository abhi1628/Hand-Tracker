import cv2
import numpy as np
import os
import time
import HandTrackingModule as htm

wcam, hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

folderpath = 'C:\\Users\\Global\\Documents\\ocv\\HandTrackingProject\\FingerImages'
mylist = os.listdir(folderpath)
#print(mylist)
overlaylist = []
for impath in mylist:
    image = cv2.imread(f'{folderpath}/{impath}')
    #print(f'{folderpath}/{impath}')
    overlaylist.append(image)

print(len(overlaylist))
ptime = 0
ctime = 0

detector = htm.handDetector(detectionCon = 0.75)
tipids = [4,8,12,16,20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw = False)

    if len(lmlist) != 0:
        fingers = []
        if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
                fingers.append(1)
        else:
            fingers.append(0)

        for id in range (1,5):
            if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalfingers  = fingers.count(1)
        print(totalfingers)

        h, w, c = overlaylist[totalfingers-1].shape
        img [0:h, 0:w] = overlaylist[totalfingers-1]

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalfingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),5)

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)),(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)