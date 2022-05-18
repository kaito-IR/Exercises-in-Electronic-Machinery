import cv2
import adjust
import datetime
adjust = adjust.adjust()
face_cascade_path = 'haarcascade_frontalface_default.xml'#顔認識のためのデータの読み込み
face_cascade = cv2.CascadeClassifier(face_cascade_path)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));#動作の軽量化のためカメラの設定を変更
cap.set(cv2.CAP_PROP_BUFFERSIZE, 7)#処理落ち軽減のためバッファを拡張
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
Kf = 30
Kf_Max = 50
ratio = 0.05
ChangeGrayFrame = False
ChangeBinaryFrame = False
ChangeAvatarFrame = False
ChangeHSVFrame = False
ChangeMosaicFrame = False

def BeautifulSkinFilter():#顔認識からの各種フィルタ処理を施すメイン関数
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))#処理の軽減のため映像を半分にリサイズ
    before = frame.copy()
    # バイラテラルフィルタ
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)#カメラの映像から顔の要素を抽出し，抽出した要素の座標を返す
    if ChangeGrayFrame:#各種フィルタのフラグを確認
        frame = gray
    elif ChangeBinaryFrame:
        ret2,frame = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    elif ChangeAvatarFrame:
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    elif ChangeHSVFrame:
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    if len(faces) != 0:
        if ChangeMosaicFrame:#モザイクフラグが立っていればモザイク処理を施す
            for x,y,w,h in faces:
                small = cv2.resize(frame[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
                frame[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        else:
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = frame[y: y + h, x: x + w]#全体の画像から顔の部分のみを抽出
                face_gray = gray[y: y + h, x: x + w]
                face = adjust.adjust(face,1.1,Kf)
                frame = cv2.blur(frame,(2,2))
                dst = cv2.bilateralFilter(face, Kf, sigmaColor=1.2*(Kf+70), sigmaSpace=1.2*(Kf+20))
                frame[y:y + h,x: x + w] = dst#美肌処理を施した顔を全体の画像に貼り付ける
    return frame,before

def ChangeValueTrackbar(position):
    global Kf
    Kf = position
    frame = BeautifulSkinFilter()
    cv2.imshow("after",frame)

cv2.namedWindow("after")
cv2.createTrackbar("FilterStrength","after",Kf,Kf_Max,ChangeValueTrackbar)
while(1):
    # バイラテラルフィルタ
    frame,before = BeautifulSkinFilter()
    cv2.imshow("after",frame)
    key = cv2.waitKey(1)
    if key == 27:#escキーが押された時
        break
    elif key == ord('s'):
        dt_now = datetime.datetime.now()
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"_after.png",frame)
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+"_before.png",before)
    elif key == ord('g'):
        ChangeGrayFrame = not ChangeGrayFrame
        ChangeMosaicFrame = False
        ChangeBinaryFrame = False
        ChangeAvatarFrame = False
        ChangeHSVFrame = False
    elif key == ord('b'):
        ChangeBinaryFrame = not ChangeBinaryFrame
        ChangeMosaicFrame = False
        ChangeGrayFrame = False
        ChangeAvatarFrame = False
        ChangeHSVFrame = False
    elif key == ord('a'):
        ChangeAvatarFrame = not ChangeAvatarFrame
        ChangeMosaicFrame = False
        ChangeGrayFrame = False
        ChangeBinaryFrame = False
        ChangeHSVFrame = False
    elif key == ord('h'):
        ChangeHSVFrame = not ChangeHSVFrame
        ChangeMosaicFrame = False
        ChangeGrayFrame = False
        ChangeBinaryFrame = False
        ChangeAvatarFrame = False
    elif key == ord('m'):
        ChangeMosaicFrame = not ChangeMosaicFrame
        ChangeGrayFrame = False
        ChangeBinaryFrame = False
        ChangeAvatarFrame = False
        ChangeHSVFrame = False
        
cv2.destroyAllWindows()
cap.release()