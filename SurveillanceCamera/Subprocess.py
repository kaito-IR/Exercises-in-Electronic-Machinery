import SendGmail
Gmail = SendGmail.SendGmail("hugahugatarou@gmail.com","olrlnxqhlidabpke")
Gmail.SendMsg("不審検知","カメラに不審な動きを捉えました．", "不審映像.mp4",'./不審映像.mp4','video','mp4')
del Gmail