import cv2
import numpy as np
import adjust
import time
import datetime
adjust = adjust.adjust()
face_cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)
#smile_cascade_path = 'haarcascade_smile.xml'
#smile_cascade = cv2.CascadeClassifier(smile_cascade_path)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
BeautifulSkinFilter = True
while(1):
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    # バイラテラルフィルタ
    before = frame.copy()
    if BeautifulSkinFilter:
        beforeTime = time.perf_counter()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        #smiles = smile_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        if len(faces) != 0:
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = frame[y: y + h, x: x + w]
                face_gray = gray[y: y + h, x: x + w]
                face = adjust.adjust(face,1.1,30.0)
                frame = cv2.blur(frame,(2,2))
                dst = cv2.bilateralFilter(face, 30, sigmaColor=120, sigmaSpace=80)
                frame[y:y + h,x: x + w] = dst
        #elif len(smiles) != 0:
        #    for x, y, w, h in smiles:
        #        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #        face = frame[y: y + h, x: x + w]
        #        face_gray = gray[y: y + h, x: x + w]
        #        face = adjust.adjust(face,1.1,30.0)
        #        #frame = cv2.blur(frame,(2,2))
        #        dst = cv2.bilateralFilter(face, 30, sigmaColor=120, sigmaSpace=80)
        #        frame[y:y + h,x: x + w] = dst
        #print(smiles)
    cv2.imshow("after",frame)
    afterTime = time.perf_counter()
    cv2.imshow("before",before)
    print(afterTime - beforeTime)
    key = cv2.waitKey(1)
    if key == 27:#escキーが押された時
        break
    elif key == ord('f'):
        if BeautifulSkinFilter:
            BeautifulSkinFilter = False
        else:
            BeautifulSkinFilter = True
    elif key == ord('s'):
        dt_now = datetime.datetime.now()
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png",frame)
        
cv2.destroyAllWindows()
cap.release()