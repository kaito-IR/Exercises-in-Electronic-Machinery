import cv2
import numpy as np
import time
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width,height)
while(1):
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    # バイラテラルフィルタ
    before = frame.copy()
    beforeTime = time.perf_counter()
    dst = cv2.bilateralFilter(frame, 30, sigmaColor=75, sigmaSpace=75)#sigmaColorは大きくしすぎない
    afterTime = time.perf_counter()
    cv2.imshow("before",before)
    cv2.imshow("after",dst)
    print(afterTime - beforeTime)
    if cv2.waitKey(1) != -1:
        break
cv2.destroyAllWindows()
cap.release()