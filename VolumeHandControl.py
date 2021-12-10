import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wcam, hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ctime = 0
ptime = 0

detector = htm.handDetector(detectionCon = 0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()


minvol = volrange[0]
maxvol = volrange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw = False)
    if len(lmlist) != 0:
        # print(lmlist[4], lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img, (cx, cy), 15, (0,255,255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand Range 50-300
        # Volume Range -65 - 0

        vol = np.interp(length, [50,300], [minvol, maxvol])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0,255,0), cv2.FILLED)


    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)),(40,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow('Camfeed', img)
    cv2.waitKey(1)