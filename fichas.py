import cv2 as cv
import numpy as np
cap= cv.VideoCapture(1)

lowRed= np.array([154,59,61])
upperRed= np.array([239,204,166])
lowYellow= np.array([0,75,100])
upperYellow= np.array([40,206,217])

while(1):
    ret, frame= cap.read()
    hsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    filterRed=cv.inRange(hsv, lowRed, upperRed)
    filterYellow=cv.inRange(hsv, lowYellow, upperYellow)
    filter= filterRed+filterYellow

    filter = cv.GaussianBlur(filter, (1,1), 2)
    filter = cv.medianBlur(filter,5)
    filter = cv.dilate(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    #filter = cv.dilate(filter, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)

    result = cv.bitwise_and(frame, frame, mask = filter)
    object= cv.moments(filter)
    if object['m00'] > 50000:
        cx= int(object['m10']/object['m00'])
        cy= int(object['m01']/object['m00'])
        cv.circle(result, (cx,cy), 40, (0,255,0), 2)

    cv.imshow('frame', frame)
    cv.imshow('result', result)

    w=cv.waitKey(1)
    if w==27:
        break

cap.release()
cv.destroyAllWindows
