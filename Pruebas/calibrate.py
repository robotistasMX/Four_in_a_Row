import cv2 as cv
import numpy as np
cap= cv.VideoCapture(1)
asd= 0

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
    column=[]
    ret, frame= cap.read()
    hsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lowHue = cv.getTrackbarPos('Low Hue','slider')
    lowSat = cv.getTrackbarPos('Low Sat','slider')
    lowVal = cv.getTrackbarPos('Low Val','slider')
    upperHue = cv.getTrackbarPos('Upper Hue','slider')
    upperSat = cv.getTrackbarPos('Upper Sat','slider')
    upperVal = cv.getTrackbarPos('Upper Val','slider')

    hsv = cv.GaussianBlur(hsv, (1,1), 2)
    hsv = cv.medianBlur(hsv,5)
    low= np.array([lowHue,lowSat,lowVal])
    upper= np.array([upperHue,upperSat,upperVal])
    filter=cv.inRange(hsv, low, upper)

    filter = cv.dilate(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(3,3)), iterations=1)
    filter = cv.erode(filter, cv.getStructuringElement(cv.MORPH_RECT,(5,5)), iterations=1)
    result = cv.bitwise_and(frame, frame, mask = filter)

    if asd:
        gray= cv.cvtColor(result, cv.COLOR_BGR2GRAY)
        gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,19,3)
        circles =  cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50, np.array([]), 100, 25, 10, 70)
        if circles is not None:
            try:
                for c in circles[0]:
                    cv.circle(frame, (c[0],c[1]), c[2], (0,0,255),2)
                    if(c[1]>380):
                        column.append(int(c[0]))
            except:
                pass

        column.sort()
        average= 0
        for i in range(1,len(column)):
            average+= column[i]-column[i-1]
        average= int(average/6)

        for i in range(len(column)):
            cv.line(frame, (int(column[i]+average/2), 0), (int(column[i]+average/2), 600), (0,255,0), 2)
        print(average)

    cv.line(frame, (0, 389), (800, 389), (0,255,0), 2)
    cv.imshow('frame', frame)
    cv.imshow('result', result)

    w=cv.waitKey(1)
    if w & 0xFF == ord("x"):
        asd= 1
    if w==27:
        break

cap.release()
cv.destroyAllWindows()

file= open("../data.txt", "w")
file.write(str(lowHue)+'\n'+str(lowSat)+'\n'+str(lowVal)+'\n')
file.write(str(upperHue)+'\n'+str(upperSat)+'\n'+str(upperVal)+'\n')
file.write(str(average)+'\n'+str(column[0])+'\n')

file.close()
