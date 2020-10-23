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
        cv2.circle(img_result, (x, y), 7, myColorsValue[count], cv2.FILLED)
        if x != 0 and y != 0:
            new_point.append([x, y, count])
        count += 1
    return new_point


def sort_second(val):
    return val[1]


def get_contours(image):
    _, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(img_result, cnt, -1, (255, 0, 0), 3)

            # Get corner point
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # Sort based on second value of the list
            box = sorted(box, key=sort_second)

            # calculate the top position of pencil
            x = (box[0][0] + box[1][0]) // 2
            y = ((box[0][1] + box[1][1]) // 2) - 20
    return x, y


def draw_on_canvas():

    if len(myPoint) != 0:
        for point in myPoint:
            cv2.circle(img_result, (point[0], point[1]), 6, myColorsValue[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img_result = img.copy()
    new_point = find_color()

    if len(new_point) != 0:
        for new_p in new_point:
            myPoint.append(new_p)

    draw_on_canvas()

    cv2.imshow('Video', cv2.flip(img_result, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        myPoint.clear()
