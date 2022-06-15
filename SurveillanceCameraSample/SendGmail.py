from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
class SendGmail:#Gmail送信クラス
    def __init__(self,account,password,to_account=""):#クラスをアタッチすると自動で動く．アタッチするときにGmailのアドレスとアプリパスワードを入力する
        # SMTP認証情報
        self.account = account
        self.password = password
        
        # 送受信先
        if to_account == "":
            self.to_email = self.account
        else:
            self.to_email = to_account
        self.from_email = self.account
        
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.account, self.password)
        
    def SendMsg(self,subText,msg):#何も添付しないメッセージのみの送信
        #メールのフォーマットの定義とメールアカウントへのログイン
        print("送信中")
        subject = subText#件名
        message = msg#本文
        msg = MIMEMultipart()#送信メールの作成
        msg["Subject"] = subject
        msg["To"] = self.to_email
        msg["From"] = self.from_email 
        body = MIMEText(message)
        msg.attach(body)
        self.server.send_message(msg)#メール送信
        print("送信完了")  
          
    def SendMsg_AttachVideo(self,subText,msg,AttachFileName="",AttachFilePass=""):#動画を添付するときはこれ
        #AttachFileNameは添付動画のファイル名
        #AttachFilePassは添付動画のパス
        #メールのフォーマットの定義とメールアカウントへのログイン
        print("送信中")
        subject = subText#件名
        message = msg#本文
        msg = MIMEMultipart()#送信メールの作成
        msg["Subject"] = subject
        msg["To"] = self.to_email
        msg["From"] = self.from_email 
        body = MIMEText(message)
        msg.attach(body)
        attach_file = {'name': AttachFileName, 'path': AttachFilePass}#添付データをメールに貼り付け
        attachment = MIMEBase('video', 'mp4')
        file = open(attach_file['path'], 'rb+')
        attachment.set_payload(file.read())
        file.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
        msg.attach(attachment)
        self.server.send_message(msg)#メール送信
        print("送信完了")
        
    def SendMsg_AttachImage(self,subText,msg,AttachFileName="",AttachFilePass=""):#写真を添付するときはこれ
        #AttachFileNameは添付写真のファイル名
        #AttachFilePassは添付写真のパス
        #メールのフォーマットの定義とメールアカウントへのログイン
        print("送信中")
        subject = subText#件名
        message = msg#本文
        msg = MIMEMultipart()#送信メールの作成
        msg["Subject"] = subject
        msg["To"] = self.to_email
        msg["From"] = self.from_email 
        body = MIMEText(message)
        msg.attach(body)
        attach_file = {'name': AttachFileName, 'path': AttachFilePass}#添付データをメールに貼り付け
        attachment = MIMEBase('image', 'png')
        file = open(attach_file['path'], 'rb+')
        attachment.set_payload(file.read())
        file.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
        msg.attach(attachment)
        self.server.send_message(msg)#メール送信
        print("送信完了")
        
    def __del__(self):#クラスを廃棄するとき自動で実行
        self.server.quit()