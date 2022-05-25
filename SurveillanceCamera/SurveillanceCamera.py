# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
import FrameSub

FSub = FrameSub.frame_sub()#クラスの読み込み
DetectionMoment = 500#フレーム差分の値がこの値以上になると動体検知
DetectionWaitTime = 0#連続検知を避けるためのクールタイム
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
subject = "不審検知"#件名
message = "カメラに不審な物体を捉えました"#本文

# 動画ファイルのキャプチャ
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));#動作の軽量化のためカメラの設定を変更
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)#ラグ軽減のためバッファを無くす
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
Grays = []
for i in range(3):
    # フレーム取得してグレースケール変換を3回繰り返す
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    Grays.append(gray)

while(cap.isOpened()):
    # フレーム間差分を計算
    mask = FSub.frame_sub(Grays[0], Grays[1], Grays[2], th=30)
    Moment = cv2.countNonZero(mask)#白い部分のピクセル数を検出
    print(Moment)
    #print(time.perf_counter() - DetectionWaitTime)
    if Moment > DetectionMoment and (time.perf_counter() - DetectionWaitTime >= 30.0 or DetectionWaitTime == 0):#白い部分のピクセル数が閾値を超え，かつクールタイムが終了していれば動体を検知
        DetectionWaitTime = time.perf_counter()#時間を更新し連続検知を避ける
        dt_now = datetime.datetime.now()#時間を取得
        cv2.imwrite(""+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png",frame)#画像ファイルを保存
        msg = MIMEMultipart()#送信メールの作成
        msg["Subject"] = subject
        msg["To"] = to_email
        msg["From"] = from_email 
        body = MIMEText(message)
        msg.attach(body)
        attach_file = {'name': dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png", 'path': './'+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')+".png"} # nameは添付ファイル名。pathは添付ファイルの位置を指定
        attachment = MIMEBase('image', 'png')
        file = open(attach_file['path'], 'rb+')
        attachment.set_payload(file.read())
        file.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
        msg.attach(attachment)
        server.send_message(msg)#メール送信(結構重い処理なのか数秒動作が止まる)
    # 結果を表示
    ret,frame = cap.read()
    frame = cv2.resize(frame,dsize=(int(width/2),int(height/2)))#処理軽減のため画像のサイズを半分に
    cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)

    # 3枚のフレームを更新
    Grays[0] = Grays[1]
    Grays[1] = Grays[2]
    Grays[2] = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
server.quit()
cap.release()
cv2.destroyAllWindows()