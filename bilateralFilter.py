import cv2
import numpy as np

img = cv2.imread("OldMan.jpg")

# バイラテラルフィルタ
dst = cv2.bilateralFilter(img, 15, sigmaColor=75, sigmaSpace=75)#sigmaColorは大きくしすぎない
cv2.imshow("",dst)
cv2.waitKey(0)