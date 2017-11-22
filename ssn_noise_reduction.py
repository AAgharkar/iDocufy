import cv2,os
import numpy as np
from PIL import Image,ImageEnhance
def mean_using_mb(image):
    median = cv2.GaussianBlur(image.copy(), (1,3),0)
    res = abs(image - median)
    res_mean = np.mean(res)
    return res_mean
def process_image(image, val):
    img = cv2.GaussianBlur(image.copy(), (1, 3),0)
    dst = cv2.fastNlMeansDenoising(img.copy(), None, val, 7, 21)
    kernel = np.ones((2, 2), np.float32)
    erode = cv2.erode(dst, kernel, iterations=1)
    img2pil = Image.fromarray(erode)
    enhancer = ImageEnhance.Sharpness(img2pil)
    sharp = enhancer.enhance(3.5)
    img2cv = np.asarray(sharp)
    return img2cv
def image_conversion_smooth(path):
    img = cv2.imread(path)
    head, tail = os.path.split(path)
    pImg = process_image(img, 13)
    for i in list(range(5)):  # to Iterate again
        mean = mean_using_mb(pImg)
        if (mean > 65.0):
            pImg = process_image(pImg, 20)
        else:
            break
    cv2.imwrite("static\\" + tail, pImg)
    return "static\\" + tail