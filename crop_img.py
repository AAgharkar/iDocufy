import cv2,os
import numpy as np
import noise_reduction
from changePerspective import get_new_size
from changePerspective import get_zero_cordinates

def get_cropped_image(IMAGE_PATH):
    img = cv2.imread(IMAGE_PATH)
    (h, w) = img.shape[:2]
    r = 960 / float(w)
    dim = (960, int(h * r))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # img = cv2.resize(img, (640, 640), fx=0.50, fy=0.50)
    edged = cv2.Canny(img, 40, 250)
    # cv2.imshow("Edges", edged)
    # cv2.waitKey(0)

    # applying closing function
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 20))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("Closed", closed)
    # cv2.waitKey(0)

    # finding_contours
    _, contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    c = max(contour_sizes, key=lambda x: x[0])[1]
    # for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    # cv2.imshow('approx', img)
    # cv2.waitKey(0)
    x, y, w, h = cv2.boundingRect(approx)
    new_img = img[y:y + h, x:x + w]
    # cv2.imwrite('7_img.png', new_img)
    rect = cv2.minAreaRect(approx)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    # cv2.rectangle(image,(x,y),(x+5,y+5),(255,0,0),3)
    # print(w,h)
    # print(box)
    if len(box) > 3:
        ogPoints = []
        ogPoints.append(box[2])
        ogPoints.append(box[3])
        ogPoints.append(box[1])
        ogPoints.append(box[0])
        # print(ogPoints)
        # print(ogPoints, '\n', box)
        newPoints = get_zero_cordinates(ogPoints)
        # print(newPoints)
        npOgPnts = np.float32(ogPoints)
        npNwPnts = np.float32(newPoints)
        # print(newPoints)
        w, h = get_new_size(newPoints)
        perspectiveTransformMatrix = cv2.getPerspectiveTransform(npOgPnts, npNwPnts)
        result = cv2.warpPerspective(img, perspectiveTransformMatrix, (w, h))
        # cv2.imwrite('2_img.png', result)

        # cv2.imshow("result", result)
        # cv2.waitKey(0)

        # cv2.destroyAllWindows()
    else:
        print("No Four points")
    head,tail=os.path.split(IMAGE_PATH)
    cv2.imwrite('Cropping\\'+tail,new_img)
    image_path=noise_reduction.image_conversion_smooth('Cropping\\'+tail)
    return image_path