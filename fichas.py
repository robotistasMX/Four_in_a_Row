import cv2 as cv
import numpy as np
cap= cv.VideoCapture(0)

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
    gray= cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,19,3)
    circles =  cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 40, np.array([]), 100, 37, 5, 50)

    circulos=0
    if circles is not None:
        try:
            for c in circles[0]:
                cv.circle(frame, (c[0],c[1]), c[2], (0,255,0),2)
                circulos=circulos+1
                print("Coordenada X: " + str(c[0]))
                print("Coordenada Y: " + str(c[1]))
            print(circulos)
        except:
            pass

    cv.imshow('frame', frame)
    cv.imshow('circles', gray)
    cv.imshow('result',result)

    w=cv.waitKey(1)
    if w==27:
        break
    if w & 0xFF == ord("x"):
        print("asdfg")
        hsv= cv.cvtColor(result, cv.COLOR_BGR2HSV)
        filterRed=cv.inRange(hsv, lowRed, upperRed)
        filterRed = cv.bitwise_and(frame, frame, mask = filterRed)

cap.release()
cv.destroyAllWindows
