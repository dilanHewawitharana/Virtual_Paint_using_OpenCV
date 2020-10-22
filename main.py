import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 100)  # Set Brightness

myColors = [[96, 172, 3, 133, 255, 255],
            [0, 191, 42, 3, 255, 249],
            [9, 252, 57, 14, 255, 255],
            [17, 169, 69, 28, 255, 255],
            [60, 141, 31, 95, 255, 255]]

myColorsValue = [[153, 76, 0],
                 [0, 0, 204],
                 [0, 102, 204],
                 [0, 255, 255],
                 [0, 102, 0]]

myPoint = []  # [x, y, colorID]


def find_color():
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_point = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = get_contours(mask)
        cv2.circle(img_result, (x, y), 10, myColorsValue[count], cv2.FILLED)
        if x != 0 and y != 0:
            new_point.append([x, y, count])
        count += 1
    return new_point


def get_contours(image):
    _, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            cv2.drawContours(img_result, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print(len(approx))
            obj_cor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def draw_on_canvas():
    for point in myPoint:
        cv2.circle(img_result, (point[0], point[1]), 10, myColorsValue[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img_result = img.copy()
    new_point = find_color()

    if len(new_point) != 0:
        for new_p in new_point:
            myPoint.append(new_p)

    if len(myPoint) != 0:
        draw_on_canvas()

    cv2.imshow('Video', img_result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
