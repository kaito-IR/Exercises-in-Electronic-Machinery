import cv2
import numpy as np
import datetime
import HandTracker

hand = HandTracker.handTracker()

def main():#メイン関数．基本的な処理は全部ここでやる
    global FingersPos_old
    global DoubleHand
    ret,frame = cap.read()
    #frame = cv2.resize(frame,dsize=(width,height))#処理軽減のため画像のサイズを半分に
    frame = hand.handsFinder(frame)
    lmList = hand.positionFinder(frame)
    Blue = cv2.getTrackbarPos("B","Camera")#トラックバーの値を取得
    Green = cv2.getTrackbarPos("G","Camera")
    Red = cv2.getTrackbarPos("R","Camera")
    FingersColor[int(fingerNo/4-1)] = [Blue,Green,Red]
    cor = FingersColor[int(fingerNo/4-1)]
    Size = cv2.getTrackbarPos("Size","Camera")
    Fps = cap.get(cv2.CAP_PROP_FPS)
    if len(lmList) != 0 and Size != 0:
        if Draw:#描画フラグが立ってれば描画
            if len(lmList) < 42:
                if DoubleHand:
                    FingersPos_old = [[],[],[],[],[],[],[],[],[],[]]
                DoubleHand = False
            else:
                DoubleHand = True
                
            if AllFingersDraw:
                for i in range(4,len(lmList),4):
                    if i > 20:
                        i = i + 1
                    cor = FingersColor[int(i/4-1)]
                    cv2.circle(frame,(lmList[i][1],lmList[i][2]), 15 , (255,255,255), cv2.FILLED)
                    if len(FingersPos_old[int(i/4-1)]) == 0 or FingersPos_old[int(i/4-1)][0] == 0:
                        cv2.circle(img,(lmList[i][1],lmList[i][2]),int(Size/2),cor,-1)
                    else:
                        cv2.line(img,FingersPos_old[int(i/4-1)],(lmList[i][1],lmList[i][2]),cor,Size)
            else:
                cv2.circle(frame,(lmList[fingerNo][1],lmList[fingerNo][2]), 15 , (255,255,255), cv2.FILLED)
                if len(FingersPos_old[int(fingerNo/4-1)]) == 0 or FingersPos_old[int(fingerNo/4-1)][0] == 0:
                    cv2.circle(img,(lmList[fingerNo][1],lmList[fingerNo][2]),int(Size/2),cor,-1)
                else:
                    #丸だと綺麗に軌跡を描けないので，前回認識時の座標を記録し，その座標と今の座標との間を直線で結ぶことで軌跡を描く
                    cv2.line(img,FingersPos_old[int(fingerNo/4-1)],(lmList[fingerNo][1],lmList[fingerNo][2]),cor,Size)
        
        if len(lmList) < 42:
            for i in range(22):
                lmList.append([0,0,0])
        for i in range(4,42,4):
            if i > 20:
                i = i + 1
            FingersPos_old[int(i/4-1)] = [lmList[i][1],lmList[i][2]]#座標を記録
    else:#手を認識出来なかったら記録した座標を初期化
        FingersPos_old = [[],[],[],[],[],[],[],[],[],[]]
        
    frame = cv2.bitwise_and(frame,img)#カメラの映像とキャンパスの映像を合体
    frame = cv2.flip(frame,1)
    
    cv2.putText(frame,"B:"+str(FingersColor[int(fingerNo/4-1)][0]),(0,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1,cv2.LINE_AA)#トラックバーから取得した値を表示
    cv2.putText(frame,"G:"+str(FingersColor[int(fingerNo/4-1)][1]),(0,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1,cv2.LINE_AA)
    cv2.putText(frame,"R:"+str(FingersColor[int(fingerNo/4-1)][2]),(0,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frame,"Size:"+str(Size),(0,120),cv2.FONT_HERSHEY_SIMPLEX,1,FingersColor[int(fingerNo/4-1)],1,cv2.LINE_AA)
    cv2.putText(frame,"FPS:"+str(Fps),(1135,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1,cv2.LINE_AA)#FPSを表示
    cv2.rectangle(frame,(0,CursorPos-30),(120,CursorPos),(0,0,0),2)#カーソル表示
    
    if len(lmList) != 0:
        for i in range(4,len(lmList),4):
            if i > 20:
                i = i + 1
            x = width - lmList[i][1]
            y = lmList[i][2]
            cv2.putText(frame,str(int(i/4)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,2.0,FingersColor[int(i/4-1)],2)
            
    cv2.imshow('Camera', frame)
    #cv2.imshow('Canvas',img)

def ChangeBlue(pos):#トラックバーが動いた時のコールバック関数
    if pos < 0:
        cv2.setTrackbarPos("B","Camera",0)
    elif pos > 255:
        cv2.setTrackbarPos("B","Camera",255)
    else:
        cv2.setTrackbarPos("B","Camera",pos)
    main()
    
def ChangeGreen(pos):#トラックバーが動いた時のコールバック関数
    if pos < 0:
        cv2.setTrackbarPos("G","Camera",0)
    elif pos > 255:
        cv2.setTrackbarPos("G","Camera",255)
    else:
        cv2.setTrackbarPos("G","Camera",pos)
    main()
    
def ChangeRed(pos):#トラックバーが動いた時のコールバック関数
    if pos < 0:
        cv2.setTrackbarPos("R","Camera",0)
    elif pos > 255:
        cv2.setTrackbarPos("R","Camera",255)
    else:
        cv2.setTrackbarPos("R","Camera",pos)
    main()

def ChangeSize(pos):#トラックバーが動いた時のコールバック関数
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
img = np.full((height,width,3),255,np.uint8)#線を描画するキャンパスを作成
cv2.namedWindow('Camera')
cv2.createTrackbar('B','Camera',0,255,ChangeBlue)#カラーパレットをトラックバーで表示
cv2.createTrackbar('G','Camera',255,255,ChangeGreen)
cv2.createTrackbar('R','Camera',0,255,ChangeRed)
cv2.createTrackbar('Size','Camera',30,90,ChangeSize)#ペンのサイズを変更するトラックバーを表示
Draw = True
DoubleHand = False
AllFingersDraw = False
FingersColor = [[255,0,0],[0,255,0],[0,0,255],[255,0,255],[255,255,0],[128,128,128],[128,128,0],[128,0,0],[0,128,0],[0,0,128]]
FingersPos_old = [[],[],[],[],[],[],[],[],[],[]]
CursorPos = 35

while True:
    main()
    key = cv2.waitKey(1)
    #if key != -1:
    #    print(key)
    if key == 0:#上矢印キーが押されたらカーソルを上に移動
        CursorPos = CursorPos - 30
        if CursorPos < 35:
            CursorPos = 125
            
    elif key == 1:#下矢印キーが押されたらカーソルを下に移動
        CursorPos = CursorPos + 30
        if CursorPos > 125:
            CursorPos = 35
            
    elif key == 2:#左矢印キーが押されたらカーソルで選択されている要素のトラックバーの値を1ずつ減らす
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
                
    elif key == 3:#右矢印キーが押されたらカーソルで選択されている要素のトラックバーの値を1ずつ増やす
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
            
    elif key == 49:#親指描画モードに切り替え
        fingerNo = 4
        cv2.setTrackbarPos("B",'Camera',FingersColor[int(fingerNo/4-1)][0])
        cv2.setTrackbarPos("G",'Camera',FingersColor[int(fingerNo/4-1)][1])
        cv2.setTrackbarPos("R",'Camera',FingersColor[int(fingerNo/4-1)][2])
        
    elif key == 50:#人差し指描画モードに切り替え
        fingerNo = 8
        cv2.setTrackbarPos("B",'Camera',FingersColor[int(fingerNo/4-1)][0])
        cv2.setTrackbarPos("G",'Camera',FingersColor[int(fingerNo/4-1)][1])
        cv2.setTrackbarPos("R",'Camera',FingersColor[int(fingerNo/4-1)][2])
        
    elif key == 51:#中指描画モードに切り替え
        fingerNo = 12
        cv2.setTrackbarPos("B",'Camera',FingersColor[int(fingerNo/4-1)][0])
        cv2.setTrackbarPos("G",'Camera',FingersColor[int(fingerNo/4-1)][1])
        cv2.setTrackbarPos("R",'Camera',FingersColor[int(fingerNo/4-1)][2])
        
    elif key == 52:#薬指描画モードに切り替え
        fingerNo = 16
        cv2.setTrackbarPos("B",'Camera',FingersColor[int(fingerNo/4-1)][0])
        cv2.setTrackbarPos("G",'Camera',FingersColor[int(fingerNo/4-1)][1])
        cv2.setTrackbarPos("R",'Camera',FingersColor[int(fingerNo/4-1)][2])
        
    elif key == 53:#小指描画モードに切り替え
        fingerNo = 20
        cv2.setTrackbarPos("B",'Camera',FingersColor[int(fingerNo/4-1)][0])
        cv2.setTrackbarPos("G",'Camera',FingersColor[int(fingerNo/4-1)][1])
        cv2.setTrackbarPos("R",'Camera',FingersColor[int(fingerNo/4-1)][2])
       
    elif key == ord('a'):#bキーが押されたらペンの色を青に変更
        AllFingersDraw = not AllFingersDraw
        
    elif key == ord('b'):#bキーが押されたらペンの色を青に変更
        cv2.setTrackbarPos("B",'Camera',255)
        cv2.setTrackbarPos("G",'Camera',0)
        cv2.setTrackbarPos("R",'Camera',0)
        
    elif key == ord('c'):#cキーが押されたらペンの色をシアンに変更
        cv2.setTrackbarPos("B",'Camera',255)
        cv2.setTrackbarPos("G",'Camera',255)
        cv2.setTrackbarPos("R",'Camera',0)
        
    elif key == ord('d'):#dキーが押されたら描画フラグを切り替え
        Draw = not Draw
        
    elif key == ord('e'):#eキーが押されたら画面全体をリセット
        img = np.full((height,width,3),255,np.uint8)
        
    elif key == ord('g'):#gキーが押されたらペンの色を緑に変更
        cv2.setTrackbarPos("B",'Camera',0)
        cv2.setTrackbarPos("G",'Camera',255)
        cv2.setTrackbarPos("R",'Camera',0)
        
    elif key == ord('p'):#pキーが押されたらペンの色をピンクに変更
        cv2.setTrackbarPos("B",'Camera',255)
        cv2.setTrackbarPos("G",'Camera',0)
        cv2.setTrackbarPos("R",'Camera',255)
        
    elif key == 27 or key == ord('q'):#escキーかqキーが押されたらプログラム終了
        break
    
    elif key == ord('r'):#rキーが押されたらペンの色を赤に変更
        cv2.setTrackbarPos("B",'Camera',0)
        cv2.setTrackbarPos("G",'Camera',0)
        cv2.setTrackbarPos("R",'Camera',255)
        
    elif key == ord('s'):#sキーが押されたら画面をスクショして保存
        dt_now = datetime.datetime.now()
        ret,frame = cap.read()
        frame = cv2.bitwise_and(frame,img)
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png",frame)
        
    elif key == 127 or key == ord('w'):#バックスペースキーかwキーが押されたら消しゴムモード(ペンの色を白に)に切り替え
        cv2.setTrackbarPos("B",'Camera',255)
        cv2.setTrackbarPos("G",'Camera',255)
        cv2.setTrackbarPos("R",'Camera',255)
        
    elif key == ord('y'):#yキーが押されたらペンの色を黄色に変更
        cv2.setTrackbarPos("B",'Camera',0)
        cv2.setTrackbarPos("G",'Camera',255)
        cv2.setTrackbarPos("R",'Camera',255)
