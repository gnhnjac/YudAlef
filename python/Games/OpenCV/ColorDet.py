import numpy as np
import cv2
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # canny = cv2.Canny(frame, 120, 120)

    # cv2.imshow('frame', frame)
    # cv2.imshow('canny', canny)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # red_low = np.array([150, 120, 0])
    # red_high = np.array([180, 255, 255])

    red_low = np.array([160, 100, 100])
    red_high = np.array([179, 255, 255])

    mask = cv2.inRange(hsv, red_low, red_high)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    # slider
    kernel = np.ones((5, 5), np.uint8)

    dilation = cv2.dilate(mask, kernel, iterations=1)

    # closing to mask (remove false black noise in object)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # opening to closing (remove false background noise)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    cv2.imshow('frame', frame)

    cv2.imshow('res', res)

    cv2.imshow('mask', mask)

    cv2.imshow('dil', dilation)

    cv2.imshow('op', opening)

    cv2.imshow('clo', closing)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()