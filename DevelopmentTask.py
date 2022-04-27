import cv2
import numpy as np
import adjust
import time
adjust = adjust.adjust()
face_cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
while(1):
    ret,frame = cap.read()
    dst = np.zeros((int(height/2),int(width/2)),dtype=np.uint8)
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    # バイラテラルフィルタ
    before = frame.copy()
    beforeTime = time.perf_counter()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = frame[y: y + h, x: x + w]
        face_gray = gray[y: y + h, x: x + w]
        face = adjust.adjust(face,1.1,30.0)
        #frame = cv2.blur(frame,(2,2))
        dst = cv2.bilateralFilter(face, 30, sigmaColor=120, sigmaSpace=80)
        frame[y:y + h,x: x + w] = dst
    cv2.imshow("after",frame)
    afterTime = time.perf_counter()
    cv2.imshow("before",before)
    print(afterTime - beforeTime)
    if cv2.waitKey(1) != -1:
        break
cv2.destroyAllWindows()
cap.release()