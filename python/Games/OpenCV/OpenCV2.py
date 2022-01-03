import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()

    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    template = cv2.imread('template.png', 0)

    w, h = template.shape[::-1]

    res = cv2.matchTemplate(grayimg, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0, 0, 0), 2)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()