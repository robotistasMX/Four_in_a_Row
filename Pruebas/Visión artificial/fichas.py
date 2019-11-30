import cv2 as cv
import numpy as np
import time
cap= cv.VideoCapture(0)

#lowRed= np.array([133,91,30])
#upperRed= np.array([215,213,255])
#lowBlack= np.array([38,5,3])
#upperBlack= np.array([162,192,127])
lowRed= np.array([164,77,19])
upperRed= np.array([206,243,204])
lowBlack= np.array([12,0,0])
upperBlack= np.array([243,169,65])
grid=[]
for i in range(7):
    grid.append(list())
    for j in range(7):
        grid[i].append(0)

while(1):
    ret, frame= cap.read()
    hsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    circles=[[],[],[],[],[],[],[]]

    #Fichas rojas
    filterRed=cv.inRange(hsv, lowRed, upperRed)
    filterRed = cv.GaussianBlur(filterRed, (1,1), 2)
    filterRed = cv.medianBlur(filterRed,5)
    filterRed = cv.dilate(filterRed, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    filterRed = cv.erode(filterRed, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
    filterRed = cv.erode(filterRed, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    resultRed = cv.bitwise_and(frame, frame, mask = filterRed)

    gray= cv.cvtColor(resultRed, cv.COLOR_BGR2GRAY)
    gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,19,3)
    circlesRed =  cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50, np.array([]), 100, 20, 10, 70)
    if circlesRed is not None:
        try:
            for c in circlesRed[0]:
                cv.circle(frame, (c[0],c[1]), c[2], (0,0,255),2)
                column= int((c[0]-20)/80)
                circles[column].append([c[1], 1])
        except:
            pass

    #Fichas negras
    filterBlack=cv.inRange(hsv, lowBlack, upperBlack)
    filterBlack = cv.GaussianBlur(filterBlack, (1,1), 2)
    filterBlack = cv.medianBlur(filterBlack,5)
    filterBlack = cv.dilate(filterBlack, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    filterBlack = cv.erode(filterBlack, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
    filterBlack = cv.erode(filterBlack, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    resultBlack = cv.bitwise_and(frame, frame, mask = filterBlack)

    gray= cv.cvtColor(resultBlack, cv.COLOR_BGR2GRAY)
    gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,19,3)
    circlesBlack =  cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 40, np.array([]), 100, 20, 5, 50)
    if circlesBlack is not None:
        try:
            for c in circlesBlack[0]:
                cv.circle(frame, (c[0],c[1]), c[2], (0,0,0),2)
                column= int((c[0]-20)/80)
                circles[column].append([c[1], 2])
        except:
            pass

    cant=0
    for i in range(7):
        cant+= len(circles[i])
    print(cant)

    result= resultRed+resultBlack
    cv.imshow('result',result)
    cv.imshow('frame', frame)

    w=cv.waitKey(1)
    if w==27:
        break
    if w & 0xFF == ord("x"):
        print("asdfg")
        column=-1
        for i in range(7):
            circles[i].sort(reverse=True)
            for j in range(len(circles[i])):
                if grid[i][-j-1]==0 and circles[i][j][1]==1:
                    column= i
                grid[i][-j-1]= circles[i][j][1]
        print(circles)
        print(grid)
        print(column)
        time.sleep(1)

cap.release()
cv.destroyAllWindows()
