import cv2
import time
import numpy
from handTracker_py.handTracker import handTracker
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Adjust webcam resolution
camWidth, camHeight = 360, 480

cap = cv2.VideoCapture(0)  # Webcam id
cap.set(3, camWidth)
cap.set(4, camHeight)
currentT = 0
previousT = 0

detector = handTracker()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol = 0
volumeBar = 400
volumePct = 0
volumeBarDimensions = [75, 275]

while True:
    sucess, image = cap.read()
    image = detector.findHands(image)
    landmarks = detector.getPos(image, draw=False)

    if (len(landmarks) != 0):
        x1, y1 = landmarks[4][1], landmarks[4][2]
        x2, y2 = landmarks[8][1], landmarks[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # BGR colors
        cv2.circle(image, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(image, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(image, (cx, cy), 6, (0, 255, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)  # Distance between THUMB_TIP (id: 4) and INDEX_FINGER_TIP (id: 8)
        print(length)

        handRange = [30, 265]

        volumeBarDimensions = [75, 275]
        volumeBar = numpy.interp(length, handRange, volumeBarDimensions[::-1])
        volumePct = numpy.interp(length, handRange, [0, 100])

        volume.SetMasterVolumeLevelScalar(volumePct / 100.0, None)

        if (length < 35):
            cv2.circle(image, (cx, cy), 8, (0, 255, 0), cv2.FILLED)  # BGR color

    # Volume bar
    cv2.rectangle(image, (35, 75), volumeBarDimensions, (0, 255, 0), 3)
    cv2.rectangle(image, (35, int(volumeBar)), volumeBarDimensions, (0, 255, 0), cv2.FILLED)
    cv2.putText(image, f"{int(volumePct)} %", (35, 300), cv2.FONT_HERSHEY_PLAIN, 1.5, (253, 253, 253), 1)  # image, text, pos (x, y), font, scale, color, thickness)

    currentT = time.time()
    fps = 1 / (currentT - previousT)
    previousT = currentT

    cv2.putText(image, f"{str(round(fps))} fps", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (253, 253, 253), 1)  # image, text, pos (x, y), font, scale, color, thickness)

    cv2.imshow("GestureVol (CPU) Preview", image)
    cv2.waitKey(1)
