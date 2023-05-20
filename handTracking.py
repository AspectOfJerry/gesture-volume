import cv2
import mediapipe
import time

cap = cv2.VideoCapture(0)

mpHands = mediapipe.solutions.hands
hands = mpHands.Hands()
mpDraw = mediapipe.solutions.drawing_utils

previousTime = 0
currentTime = 0


while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if (results.multi_hand_landmarks):
        for handLandmarks in results.multi_hand_landmarks:
            for id, landmark in enumerate(handLandmarks.landmark):
                height, width, channel = image.shape
                cx, cy = int(landmark.x*width), int(landmark.y*height)
                print(id, cx, cy)
                cv2.circle(image, (cx, cy), 5, (0, 255, 0), 2)  # img, center, radius, color, thickness

            mpDraw.draw_landmarks(image, handLandmarks, mpHands.HAND_CONNECTIONS)

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(image, str(round(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (253, 253, 253), cv2.FILLED)  # pos, font, scale, color, thickness)

    cv2.imshow("GestureVol (CPU) Preview", image)
    cv2.waitKey(1)
