import cv2
# フレーム差分の計算
class frame_sub:
    def __init__(self):
        pass
    def frame_sub(self,img1, img2, img3, th):
        # フレームの絶対差分
        diff1 = cv2.absdiff(img1, img2)
        diff2 = cv2.absdiff(img2, img3)

        # 2つの差分画像の論理積
        diff = cv2.bitwise_and(diff1, diff2)

        # 二値化処理
        diff[diff < th] = 0
        diff[diff >= th] = 255
        #ret,diff = cv2.threshold(diff,th,255,cv2.THRESH_OTSU)
        # メディアンフィルタ処理（ゴマ塩ノイズ除去）
        mask = cv2.medianBlur(diff, 3)

        return  mask