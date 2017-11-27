import cv2

image=cv2.imread('static/ADP Example 101817-1.jpg')
cv2.imshow('Frame',cv2.rectangle(image,(555,547),(567,575),(0,0,255),2))
cv2.waitKey(0)