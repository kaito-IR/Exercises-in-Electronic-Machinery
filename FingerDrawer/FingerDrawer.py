import cv2
import numpy as np
import datetime
import HandTracker

hand = HandTracker.handTracker()

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)#ラグ軽減のためバッファを無くす
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = int(width)
height = int(height)
fingerNo = 8#fingerNo4:親指,fingerNo8:人差し指,fingerNo12:中指,fingerNo16:薬指,fingerNo20:小指
img = np.full((height,width,3),255,np.uint8)
cv2.namedWindow('Camera')
cv2.createTrackbar('B','Camera',0,255,nothing)
cv2.createTrackbar('G','Camera',0,255,nothing)
cv2.createTrackbar('R','Camera',0,255,nothing)
cv2.createTrackbar('Size','Camera',1,30,nothing)

Draw = True

while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(width,height))#処理軽減のため画像のサイズを半分に
    frame = hand.handsFinder(frame)
    lmList = hand.positionFinder(frame,fingerNo)
    if len(lmList) != 0 and Draw:
        Blue = cv2.getTrackbarPos("B","Camera")
        Green = cv2.getTrackbarPos("G","Camera")
        Red = cv2.getTrackbarPos("R","Camera")
        Size = cv2.getTrackbarPos("Size","Camera")
        cv2.circle(img,(lmList[fingerNo][1],lmList[fingerNo][2]),Size,(Blue,Green,Red),-1)
    frame = cv2.bitwise_and(frame,img)
    cv2.imshow('Camera', frame)
    #cv2.imshow('oekaki',img)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):#escキーかqキーが押された時
        break
    elif key == ord('d'):
        Draw = not Draw
    elif key == ord('e'):
        img = np.full((height,width,3),255,np.uint8)
    elif key == ord('s'):
        dt_now = datetime.datetime.now()
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png",frame)
