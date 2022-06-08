# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import smtplib
import subprocess
import FrameSub
import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

FSub = FrameSub.frame_sub()#フレーム間差分の計算クラスを読み込み

# 動画ファイルのキャプチャ
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)#ラグ軽減のためバッファを無くす
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# 動画ファイル保存用の設定
fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
# 動画の仕様（ファイル名、fourcc, FPS, サイズ）
video = cv2.VideoWriter('./監視映像.mp4',fourcc,fps,(int(width/2), int(height/2)))#全体の監視映像の録画開始
Grays = []
VideoStartTime = time.perf_counter()#連続送信を防ぐための待ち時間
PopenProcess = False#不審映像の録画フラグ
DetectionMoment = 500#フレーム差分の値がこの値以上になると動体検知
DetectionWaitTime = 0#連続検知を避けるためのクールタイム
for i in range(3):
    # フレーム取得してグレースケール変換を3回繰り返す
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    Grays.append(gray)

while cap.isOpened():
    # フレーム間差分を計算
    mask = FSub.frame_sub(Grays[0], Grays[1], Grays[2], th=30)#フレーム差分映像の取得関数を実行．引数(差分用映像1,差分用映像2,差分用映像3,2値化の閾値)
    Moment = cv2.countNonZero(mask)#白い部分のピクセル数を検出
    if Moment > DetectionMoment and (time.perf_counter() - DetectionWaitTime >= 25.0 or DetectionWaitTime == 0):#白い部分のピクセル数が閾値を超え，かつクールタイムが終了していれば動体を検知
        video_buf = cv2.VideoWriter('./不審映像.mp4',fourcc,fps,(int(width/2), int(height/2)))#不審映像の録画を開始
        DetectionWaitTime = time.perf_counter()#時間を更新し連続検知を避ける
        PopenProcess = True#不審映像の録画フラグを立てる
    if time.perf_counter() - DetectionWaitTime >= 15.0 and PopenProcess:#不審映像の録画開始から15秒経過したら不審映像を送信するプログラムを実行(並列処理なので送信待ちしない)
        video_buf.release()
        cap.release()#不審映像の録画終了のため，一旦カメラを停止
        subprocess.Popen(["python3 Subprocess.py"],shell=True)#並列処理で不審映像を送信するプログラムを実行
        PopenProcess = False#不審映像の録画フラグを折る
        cap = cv2.VideoCapture(0)#カメラを再起動
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)#ラグ軽減のためバッファを無くす
    # 結果を表示
    ret,frame = cap.read()#カメラ映像の取得
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))#処理軽減のため画像のサイズを半分に
    # 3枚のフレームを更新
    Grays[0] = Grays[1]
    Grays[1] = Grays[2]
    Grays[2] = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    dt_now = datetime.datetime.now()#現在の年，月，日時を取得
    cv2.putText(frame,str(dt_now),(0,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)#カメラ映像に白い文字で現在の年，月，日時を描画
    cv2.putText(frame,str(dt_now),(0,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)#カメラ映像に黒い文字で現在の年，月，日時を描画
    cv2.imshow("Frame", frame)#映像を表示
    video.write(frame)# 動画を1フレームずつ保存する
    if PopenProcess:#不審映像の録画フラグが立っていたら不審映像を保存
        video_buf.write(frame)

    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("監視カメラを停止します")
        break

video.release()
if 'video_buf' in globals() or 'video_buf' in locals():
    video_buf.release()
cap.release()
#動作終了時に全体の監視映像を送信
# SMTP認証情報
account = "hugahugatarou@gmail.com"
password = "olrlnxqhlidabpke"
 
# 送受信先
to_email = account
from_email = account

#メールのフォーマットの定義とメールアカウントへのログイン
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(account, password)
msg = MIMEMultipart()#送信メールの作成
msg["Subject"] = "動作終了"
msg["To"] = to_email
msg["From"] = from_email 
body = MIMEText("監視カメラをシャットダウンしました．録画した映像はこちらになります．")
msg.attach(body)
attach_file = {'name': "監視映像.mp4", 'path': './監視映像.mp4'} # nameは添付ファイル名。pathは添付ファイルの位置を指定
attachment = MIMEBase('video', 'mp4')
file = open(attach_file['path'], 'rb+')
attachment.set_payload(file.read())
file.close()
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
msg.attach(attachment)
server.send_message(msg)#メール送信(結構重い処理なのか数秒動作が止まる)
server.quit()
cv2.destroyAllWindows()