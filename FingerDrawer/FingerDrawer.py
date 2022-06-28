import cv2
import numpy as np
import datetime
import HandTracker

hand = HandTracker.handTracker()

def nothing(x):
    pass

def main():
    global Pos_old
    ret,frame = cap.read()
    #frame = cv2.resize(frame,dsize=(width,height))#処理軽減のため画像のサイズを半分に
    frame = hand.handsFinder(frame)
    lmList = hand.positionFinder(frame,fingerNo)
    Blue = cv2.getTrackbarPos("B","Camera")
    Green = cv2.getTrackbarPos("G","Camera")
    Red = cv2.getTrackbarPos("R","Camera")
    Size = cv2.getTrackbarPos("Size","Camera")
    Fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.putText(frame,"B:"+str(Blue),(0,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(frame,"G:"+str(Green),(0,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1,cv2.LINE_AA)
    cv2.putText(frame,"R:"+str(Red),(0,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frame,"Size:"+str(Size),(0,120),cv2.FONT_HERSHEY_SIMPLEX,1,(Blue,Green,Red),1,cv2.LINE_AA)
    cv2.putText(frame,"FPS:"+str(Fps),(1135,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1,cv2.LINE_AA)
    cv2.rectangle(frame,(0,CursorPos-30),(120,CursorPos),(0,0,0),2)
    if len(lmList) != 0 and Size != 0:
        if Draw:
            if len(Pos_old) == 0:
                cv2.circle(img,(lmList[fingerNo][1],lmList[fingerNo][2]),int(Size/2),(Blue,Green,Red),-1)
            else:
                cv2.line(img,(Pos_old[0],Pos_old[1]),(lmList[fingerNo][1],lmList[fingerNo][2]),(Blue,Green,Red),Size)
        Pos_old = [lmList[fingerNo][1],lmList[fingerNo][2]]
    else:
        Pos_old = []
        
    frame = cv2.bitwise_and(frame,img)
    cv2.imshow('Camera', frame)

def ChangeBlue(pos):
    if pos < 0:
        cv2.setTrackbarPos("B","Camera",0)
    elif pos > 255:
        cv2.setTrackbarPos("B","Camera",255)
    else:
        cv2.setTrackbarPos("B","Camera",pos)
    main()
    
def ChangeGreen(pos):
    if pos < 0:
        cv2.setTrackbarPos("G","Camera",0)
    elif pos > 255:
        cv2.setTrackbarPos("G","Camera",255)
    else:
        cv2.setTrackbarPos("G","Camera",pos)
    main()
    
def ChangeRed(pos):
    if pos < 0:
        cv2.setTrackbarPos("R","Camera",0)
    elif pos > 255:
        cv2.setTrackbarPos("R","Camera",255)
    else:
        cv2.setTrackbarPos("R","Camera",pos)
    main()

def ChangeSize(pos):
    if pos <= 0:
        cv2.setTrackbarPos("Size","Camera",1)
    elif pos > 90:
        cv2.setTrackbarPos("Size","Camera",90)
    else:
        cv2.setTrackbarPos("Size","Camera",pos)
    main()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)#ラグ軽減のためバッファを無くす
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = int(width)
height = int(height)
fingerNo = 8#fingerNo4:親指,fingerNo8:人差し指,fingerNo12:中指,fingerNo16:薬指,fingerNo20:小指
img = np.full((height,width,3),255,np.uint8)
cv2.namedWindow('Camera')
cv2.createTrackbar('B','Camera',255,255,ChangeBlue)
cv2.createTrackbar('G','Camera',0,255,ChangeGreen)
cv2.createTrackbar('R','Camera',255,255,ChangeRed)
cv2.createTrackbar('Size','Camera',30,90,ChangeSize)
Draw = True
Pos_old = []
CursorPos = 35

while True:
    main()
    key = cv2.waitKey(1)
    if key != -1:
        print(key)
    if key == 27 or key == ord('q'):#escキーかqキーが押された時
        break
    elif key == 0:
        CursorPos = CursorPos - 30
        if CursorPos < 35:
            CursorPos = 125
    elif key == 1:
        CursorPos = CursorPos + 30
        if CursorPos > 125:
            CursorPos = 35
    elif key == 2:
        if (CursorPos - 35)/30 == 0:
            pos = cv2.getTrackbarPos("B","Camera")
            cv2.setTrackbarPos("B",'Camera',pos-1)
        elif (CursorPos - 35)/30 == 1:
            pos = cv2.getTrackbarPos("G","Camera")
            cv2.setTrackbarPos("G",'Camera',pos-1)
        elif (CursorPos - 35)/30 == 2:
            pos = cv2.getTrackbarPos("R","Camera")
            cv2.setTrackbarPos("R",'Camera',pos-1)
        elif (CursorPos - 35)/30 == 3:
            pos = cv2.getTrackbarPos("Size","Camera")
            if pos-1 > 0:
                cv2.setTrackbarPos("Size",'Camera',pos-1)
    elif key == 3:
        if (CursorPos - 35)/30 == 0:
            pos = cv2.getTrackbarPos("B","Camera")
            cv2.setTrackbarPos("B",'Camera',pos+1)
        elif (CursorPos - 35)/30 == 1:
            pos = cv2.getTrackbarPos("G","Camera")
            cv2.setTrackbarPos("G",'Camera',pos+1)
        elif (CursorPos - 35)/30 == 2:
            pos = cv2.getTrackbarPos("R","Camera")
            cv2.setTrackbarPos("R",'Camera',pos+1)
        elif (CursorPos - 35)/30 == 3:
            pos = cv2.getTrackbarPos("Size","Camera")
            cv2.setTrackbarPos("Size",'Camera',pos+1)
    elif key == 49:
        Pos_old = []
        fingerNo = 4
    elif key == 50:
        Pos_old = []
        fingerNo = 8
    elif key == 51:
        Pos_old = []
        fingerNo = 12
    elif key == 52:
        Pos_old = []
        fingerNo = 16
    elif key == 53:
        Pos_old = []
        fingerNo = 20
    elif key == 127 or key == ord('w'):
        cv2.setTrackbarPos("B",'Camera',255)
        cv2.setTrackbarPos("G",'Camera',255)
        cv2.setTrackbarPos("R",'Camera',255)
    elif key == ord('d'):
        Draw = not Draw
    elif key == ord('e'):
        img = np.full((height,width,3),255,np.uint8)
    elif key == ord('b'):
        cv2.setTrackbarPos("B",'Camera',255)
        cv2.setTrackbarPos("G",'Camera',0)
        cv2.setTrackbarPos("R",'Camera',0)
    elif key == ord('g'):
        cv2.setTrackbarPos("B",'Camera',0)
        cv2.setTrackbarPos("G",'Camera',255)
        cv2.setTrackbarPos("R",'Camera',0)
    elif key == ord('r'):
        cv2.setTrackbarPos("B",'Camera',0)
        cv2.setTrackbarPos("G",'Camera',0)
        cv2.setTrackbarPos("R",'Camera',255)
    elif key == ord('y'):
        cv2.setTrackbarPos("B",'Camera',0)
        cv2.setTrackbarPos("G",'Camera',255)
        cv2.setTrackbarPos("R",'Camera',255)
    elif key == ord('p'):
        cv2.setTrackbarPos("B",'Camera',255)
        cv2.setTrackbarPos("G",'Camera',0)
        cv2.setTrackbarPos("R",'Camera',255)
    elif key == ord('s'):
        dt_now = datetime.datetime.now()
        ret,frame = cap.read()
        frame = cv2.bitwise_and(frame,img)
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png",frame)
