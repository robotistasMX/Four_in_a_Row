import cv2 as cv
import numpy as np
import time
cap= cv.VideoCapture(0)

file= open("data.txt", "r")
low= np.array( [int(file.readline()),int(file.readline()),int(file.readline())] )
upper=  np.array( [int(file.readline()),int(file.readline()),int(file.readline())] )
cA= int(file.readline())
c1= int(file.readline())
rA= int(file.readline())
r1= int(file.readline())
file.close()

grid=[]
for i in range(7):
    grid.append(list())
    for j in range(6):
        grid[i].append(0)

while(1):
    ret, frame= cap.read()
    hsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #Fichas rojas
    filter =cv.inRange(hsv, low, upper)
    filter = cv.GaussianBlur(filter, (1,1), 2)
    filter = cv.medianBlur(filter,5)
    filter = cv.dilate(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    result = cv.bitwise_and(frame, frame, mask = filter)

    gray= cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,19,3)
    circles =  cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50, np.array([]), 100, 20, 10, 70)
    if circles is not None:
        try:
            for c in circles[0]:
                cv.circle(frame, (c[0],c[1]), c[2], (0,0,255),2)
            print(len(circles[0]))
        except:
            pass

    cv.imshow('result',result)
    cv.imshow('frame', frame)

    w=cv.waitKey(1)
    if w==27:
        break
    if w & 0xFF == ord("x"):
        print("asdfg")
        ans= -1
        for c in circles[0]:
            column= int((c[0]-c1+cA/2)/cA)
            row= int((c[1]-r1+rA/2)/rA)
            if grid[column][row]==0:
                ans=column
            grid[column][row]=1
        print(grid)
        print(ans)
        time.sleep(1)

cap.release()
cv.destroyAllWindows()
