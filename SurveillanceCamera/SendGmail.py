from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
class SendGmail:
    def __init__(self,account,password):
        # SMTP認証情報
        self.account = account
        self.password = password
        
        # 送受信先
        self.to_email = self.account
        self.from_email = self.account
        
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.account, self.password)
        
    def SendMsg(self,subText,msg,AttachFileName="",AttachFilePass="",FileType="",FileExtension=""):
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
        if AttachFileName != "" and AttachFilePass != "" and FileType != "" and FileExtension != "":
            attach_file = {'name': AttachFileName, 'path': AttachFilePass}
            attachment = MIMEBase(FileType, FileExtension)
            file = open(attach_file['path'], 'rb+')
            attachment.set_payload(file.read())
            file.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
            msg.attach(attachment)
        self.server.send_message(msg)#メール送信
        print("送信完了")
    def __del__(self):
        self.server.quit()