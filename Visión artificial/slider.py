import cv2 as cv
import numpy as np
cap= cv.VideoCapture(0)

def nothing(x):
    pass

cv.namedWindow('slider')
cv.createTrackbar('Low Hue', 'slider', 0, 255, nothing)
cv.createTrackbar('Low Sat', 'slider', 0, 255, nothing)
cv.createTrackbar('Low Val', 'slider', 0, 255, nothing)
cv.createTrackbar('Upper Hue', 'slider', 0, 255, nothing)
cv.createTrackbar('Upper Sat', 'slider', 0, 255, nothing)
cv.createTrackbar('Upper Val', 'slider', 0, 255, nothing)


while(1):
    ret, frame= cap.read()
    hsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lowHue = cv.getTrackbarPos('Low Hue','slider')
    lowSat = cv.getTrackbarPos('Low Sat','slider')
    lowVal = cv.getTrackbarPos('Low Val','slider')
    upperHue = cv.getTrackbarPos('Upper Hue','slider')
    upperSat = cv.getTrackbarPos('Upper Sat','slider')
    upperVal = cv.getTrackbarPos('Upper Val','slider')

    low= np.array([lowHue,lowSat,lowVal])
    upper= np.array([upperHue,upperSat,upperVal])
    filter=cv.inRange(hsv, low, upper)

    filter = cv.GaussianBlur(filter, (1,1), 2)
    filter = cv.medianBlur(filter,5)
    filter = cv.dilate(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)

    result = cv.bitwise_and(frame, frame, mask = filter)

    cv.imshow('frame', frame)
    cv.imshow('result', result)

    w=cv.waitKey(1)
    if w==27:
        break

cap.release()
cv.destroyAllWindows()
