import cv2,os
import numpy as np
from PIL import Image,ImageEnhance

def mean_using_mb(image):
    median = cv2.medianBlur(image.copy(), 3)
    res = abs(image - median)
    res_mean = np.mean(res)
    return res_mean
def process_image(image, val):
    img = cv2.GaussianBlur(image.copy(), (3, 3),0)
    dst = cv2.fastNlMeansDenoising(img.copy(), None, val, 7, 21)
    kernel = np.ones((3, 2), np.int32)
    erode = cv2.erode(dst, kernel, iterations=0)
    # img2pil = Image.fromarray(erode)
    # enhancer = ImageEnhance.Sharpness(img2pil)
    # sharp = enhancer.enhance(4.5)
    # img2cv = np.asarray(sharp)
    return erode
def image_conversion_smooth(path):
    img = cv2.imread(path)
    pImg=''
    # height, width = img.shape
    head, tail = os.path.split(path)
    mean = mean_using_mb(img)
    print(mean)
    if mean==84.5215623913:
        pImg=img
    if mean < 20:
        pImg=process_image(img,5)
    elif 20 < mean <= 46:
        pImg = process_image(img, 12)
    elif 20< mean <=64:
        pImg = process_image(img, 10)
    elif mean <=86.0:
        pImg = process_image(img, 25)
    elif mean >=87.0:
        pImg = process_image(img, 5)
    else:
        pass
    cv2.imwrite("static\\" + tail, pImg)
    return "static\\" + tail