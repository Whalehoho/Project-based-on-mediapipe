import cv2
import time
import os
import HandTrackingModule as htm

############################## 
wCam, hCam = 640, 480
##############################

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.handDetector()

tipIds = [4,8,12,16,20] 
# thumb, index finger, middle finger, ring finger, pinky finger

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList)

        fingers = []

        # Thumb (right hand)
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range (1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)

        totalFingers = fingers.count(1)
        # print(totalFingers)

        cv2.rectangle(img,(20, 225),(170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), 
                    cv2.FONT_HERSHEY_PLAIN,10, (255,0,0), 25)

    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (0, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1, (51, 255, 51), 1)
    cv2.imshow("Img",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.getWindowProperty('Img', cv2.WND_PROP_VISIBLE) < 1:  
        break
    