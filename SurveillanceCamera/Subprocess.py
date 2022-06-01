import cv2
import time
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib

# SMTP認証情報
account = "hugahugatarou@gmail.com"
password = "olrlnxqhlidabpke"
 
# 送受信先
to_email = account
from_email = account

#メールのフォーマットの定義とメールアカウントへのログイン
print("送信中")
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(account, password)
subject = "不審検知"#件名
message = "カメラに不審な物体を捉えました"#本文
msg = MIMEMultipart()#送信メールの作成
msg["Subject"] = subject
msg["To"] = to_email
msg["From"] = from_email 
body = MIMEText(message)
msg.attach(body)
attach_file = {'name': "不審映像.mp4", 'path': './不審映像.mp4'}
attachment = MIMEBase('video', 'mp4')
file = open(attach_file['path'], 'rb+')
attachment.set_payload(file.read())
file.close()
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
msg.attach(attachment)
server.send_message(msg)#メール送信(結構重い処理なのか数秒動作が止まる)
print("送信完了")