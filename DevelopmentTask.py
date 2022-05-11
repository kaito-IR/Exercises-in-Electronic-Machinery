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
cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
Kf = 30
Kf_Max = 50

def BeautifulSkinFilter():
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    # バイラテラルフィルタ
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    if len(faces) != 0:
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = frame[y: y + h, x: x + w]
            face = adjust.adjust(face,1.1,Kf)
            frame = cv2.blur(frame,(2,2))
            dst = cv2.bilateralFilter(face, Kf, sigmaColor=1.2*(Kf+70), sigmaSpace=1.2*(Kf+20))
            frame[y:y + h,x: x + w] = dst
    return frame

def ChangeValueTrackbar(position):
    global Kf
    Kf = position
    frame = BeautifulSkinFilter()
    cv2.imshow("after",frame)

cv2.namedWindow("after")
cv2.createTrackbar("FilterStrength","after",Kf,Kf_Max,ChangeValueTrackbar)
while(1):
    # バイラテラルフィルタ
    frame = BeautifulSkinFilter()
    cv2.imshow("after",frame)
    key = cv2.waitKey(1)
    if key == 27:#escキーが押された時
        break
    elif key == ord('s'):
        dt_now = datetime.datetime.now()
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png",frame)
        
cv2.destroyAllWindows()
cap.release()