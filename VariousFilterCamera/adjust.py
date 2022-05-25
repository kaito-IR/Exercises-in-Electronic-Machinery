import numpy as np
class adjust:
    def __init__(self):
        pass
    def adjust(self,img, alpha=1.0, beta=0.0):#画像のコントラストと明度に補正をかける(alpha:0.0~2.0,beta:-100.0~100.0の範囲をとる)
        # 積和演算を行う。
        dst = alpha * img + beta
        # [0, 255] でクリップし、uint8 型にする。
        return np.clip(dst, 0, 255).astype(np.uint8)