import SendGmail
import FrameSub
import cv2
import time
#フレーム間差分の計算クラスをアタッチ
FSub = FrameSub.frame_sub()
#Gmail送信クラスをアタッチ．
#Gmailのアドレス(サンプルプログラムではhugahugatarou@gmail.comとなっている)とアプリパスワード(サンプルプログラムではolrlnxqhlidabpkeとなっている)を指定
Gmail = SendGmail.SendGmail("hugahugatarou@gmail.com","olrlnxqhlidabpke")
# 動画ファイルのキャプチャ
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)#ラグ軽減のためバッファを無くす
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# 動画ファイル保存用の設定
fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
# 動画の仕様（ファイル名、fourcc, FPS, サイズ）
video = cv2.VideoWriter('./サンプル.mp4',fourcc,fps,(int(width/2), int(height/2)))#全体の監視映像の録画開始
DetectionMoment = 500#フレーム差分の値がこの値以上になると動体検知
DetectionWaitTime = 0#連続検知を避けるためのクールタイム
WAIT_TIME = 25.0#一度動作を検知したらこの秒数だけ待たないと次の検知が行われない
Grays = []
for i in range(3):
    # フレーム取得してグレースケール変換を3回繰り返す
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    Grays.append(gray)

Gmail.SendMsg("サンプル","これはサンプルです")
Gmail.SendMsg_AttachImage("サンプル","サンプル写真です","sample.png","./sample.png")
while cap.isOpened():
    # フレーム間差分を計算
    mask = FSub.frame_sub(Grays[0], Grays[1], Grays[2], th=30)#フレーム差分映像の取得関数を実行．引数(差分用映像1,差分用映像2,差分用映像3,2値化の閾値)
    Moment = cv2.countNonZero(mask)#白い部分のピクセル数を検出
    if Moment > DetectionMoment and (time.perf_counter() - DetectionWaitTime >= WAIT_TIME or DetectionWaitTime == 0):#白い部分のピクセル数が閾値を超え，かつクールタイムが終了していれば動体を検知
        DetectionWaitTime = time.perf_counter()#時間を更新し連続検知を避ける
        print("不審検知")
    
    # 結果を表示
    ret,frame = cap.read()#カメラ映像の取得
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))#処理軽減のため画像のサイズを半分に
    # 3枚のフレームを更新
    Grays[0] = Grays[1]
    Grays[1] = Grays[2]
    Grays[2] = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cv2.imshow("Frame", frame)#映像を表示
    video.write(frame)# 動画を1フレームずつ保存する   
    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("カメラを停止します")
        break
    
video.release()
cap.release()
Gmail.SendMsg_AttachVideo("サンプル","サンプルプログラムを終了したので録画データ送信します","サンプル.mp4","./サンプル.mp4")
del Gmail
cv2.destroyAllWindows()
    