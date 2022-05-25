import cv2
import numpy as np

img = cv2.imread("OldMan.jpg")

cv2.imshow("Before",img)
# バイラテラルフィルタ
#BlurImg = cv2.GaussianBlur(img,(3,3),0)
#dst = cv2.bilateralFilter(BlurImg, 30, sigmaColor=80, sigmaSpace=80)#sigmaColorは大きくしすぎない
#cv2.imshow("BlurAfter",dst)
dst = cv2.bilateralFilter(img, 30, sigmaColor=120, sigmaSpace=60)#sigmaColorは大きくしすぎない
cv2.imshow("NotBlurAfter",dst)
cv2.waitKey(0)