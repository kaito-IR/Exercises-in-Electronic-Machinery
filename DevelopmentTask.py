import cv2
import numpy as np
import adjust
import time
adjust = adjust.adjust()
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
while(1):
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    # バイラテラルフィルタ
    before = frame.copy()
    frame = adjust.adjust(frame,1.1,30.0)
    frame = cv2.blur(frame,(2,2))
    beforeTime = time.perf_counter()
    dst = cv2.bilateralFilter(frame, 30, sigmaColor=80, sigmaSpace=80)
    afterTime = time.perf_counter()
    cv2.imshow("before",before)
    cv2.imshow("after",dst)
    print(afterTime - beforeTime)
    if cv2.waitKey(1) != -1:
        break
cv2.destroyAllWindows()
cap.release()