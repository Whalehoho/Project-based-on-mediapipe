import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("./Videos/push up.mp4")
detector = pm.poseDetector()

success, img = cap.read()
H, W, _ = img.shape
out = cv2.VideoWriter("./Videos/push up.mp4_out.mp4", cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

count = 0
dir = 0
# per = 0
# perBar = 150

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (720, 480))

    # img = cv2.imread("./Images/workout10.jpg")
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    if len(lmList) != 0:

        # Angle : [50,160]
        curl=[50,160]
        squat=[70,170]
        pushup=[90,180]

        # Points
        right_arm = (12,14,16)
        left_arm = (11,13,15)
        right_leg = (24,26,28)
        left_leg = (23,25,27)
      

        angle = detector.findAngle(img,*left_arm)
        # detector.findAngle(img,*right_arm)
        per = np.interp(angle,pushup,(100,0))
        perBar = np.interp(angle, pushup, [250, 500]) 
        # print(angle,'<-->',per)

        # check for the dumbbell curls
        if per >= 60:
            if dir == 0:    # going up
                count += 0.5
                dir = 1
        if per <= 30:
            if dir == 1:    # going down
                count += 0.5
                dir = 0

        # print(count)
        cv2.rectangle(img,(50,600),(125,660),(255,0,255),cv2.FILLED)
        cv2.putText(img,f'{count}', (50,650), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),5)

    cv2.rectangle(img,(50,250),(85,500),(0,255,0),3)
    cv2.rectangle(img,(52,int(perBar)),(83,498),(88,168,88),cv2.FILLED)
    cv2.putText(img, f'{int(per)}%', (50, 550), cv2.FONT_HERSHEY_PLAIN,
                2, (0, 255, 0), 2)

    cv2.imshow("Image", img)
    out.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:  
        break

cap.release()
out.release()
cv2.destroyAllWindows()
