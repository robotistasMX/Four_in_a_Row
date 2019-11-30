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

file= open("data.txt", "w")
file.write(str(lowHue)+'\n'+str(lowSat)+'\n'+str(lowVal)+'\n')
file.write(str(upperHue)+'\n'+str(upperSat)+'\n'+str(upperVal)+'\n')

column=[]
row=[]
gray= cv.cvtColor(result, cv.COLOR_BGR2GRAY)
gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,19,3)
circles =  cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50, np.array([]), 100, 20, 10, 70)
if circles is not None:
    try:
        for c in circles[0]:
            cv.circle(frame, (c[0],c[1]), c[2], (0,0,255),2)
            column.append(int(c[0]))
            row.append(int(c[1]))
    except:
        pass

row.sort()
column.sort()

average= 0
for i in range(6,12):
    average+= column[i]-column[i-1]
average= int(average/6)
print(average)
file.write(str(average)+'\n'+str(column[5])+'\n')

average= 0
for i in range(1,6):
    average+= row[i]-row[i-1]
average= int(average/5)
print(average)
file.write(str(average)+'\n'+str(row[0])+'\n')

print(column)
print(row)

file.close()
