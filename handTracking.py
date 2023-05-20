import cv2
import time
from handTracker_py.handTracker import handTracker


previousTime = 0
currentTime = 0
cap = cv2.VideoCapture(0)
tracker = handTracker()

while True:
    success, image = cap.read()

    image = tracker.findHands(image)
    landmarks = tracker.getPos(image)

    if (len(landmarks) != 0):
        print(landmarks[4])

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(image, str(round(fps)) + " fps", (20, 70), cv2.FONT_HERSHEY_PLAIN, 1.5, (253, 253, 253), 1)  # image, text, pos (x, y), font, scale, color, thickness)

    cv2.imshow("HandTracker (CPU) Preview", image)
    cv2.waitKey(1)
