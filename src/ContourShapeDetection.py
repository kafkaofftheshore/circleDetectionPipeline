import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0,cv.CAP_DSHOW)

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")


#dummy function
empty = lambda _: True

#declare GUI for adjusting parameters
cv.namedWindow("Canny Parameters")
cv.resizeWindow("Parameters",640,240)
cv.createTrackbar("Threshold 1", "Canny Parameters",23,255,empty)
cv.createTrackbar("Threshold 2", "Canny Parameters",83,255,empty)


def predictShape(points):
    if points == 4:
        return "Rectangle or Square"
    elif points == 3:
        return "Triangle"
    elif points >= 7:
        return "Maybe a circle"
    else:
        return "Unknown"

def getContours(img,imgContour):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
  
    #filter out unneccessary contours
    for c in contours:
        area = cv.contourArea(c)
        if area > 10000:
            cv.drawContours(imgContour,c,-1,(255,0,255),5)
            perimeter = cv.arcLength(c,True)
            #approx number of points in the contour
            approx = cv.approxPolyDP(c,0.02*perimeter,True)
            print(len(approx))
            x,y,w,h = cv.boundingRect(approx)
            cv.rectangle(imgContour, (x,y), (x+w, y+h),(0,255,0),5)
            
            cv.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20),\
                cv.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            cv.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45),\
                cv.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            cv.putText(imgContour, "Shape: " + predictShape(len(approx)), (x + w + 20, y + 75),\
                cv.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            

while True:
    ret, frame = capture.read() #webcam frame shape: 480 x 640 x 3
    img = frame.copy()
    imgContour = frame.copy()
    
    #apply gaussian blur and convert to grayscale
    imgBlur = cv.GaussianBlur(img,(7,7),1)
    imgGray = cv.cvtColor(imgBlur,cv.COLOR_BGR2GRAY)
    
    #apply canny edge
    threshold1 = cv.getTrackbarPos("Threshold 1","Canny Paramaters")
    threshold2 = cv.getTrackbarPos("Threshold 2","Canny Parameters")
    imgCanny = cv.Canny(imgGray, threshold1, threshold2)
    
    #dilation to reduce noise
    kernel = np.ones((5,5))
    imgDil = cv.dilate(imgCanny, kernel, iterations=1)
    
    #apply contours
    getContours(imgDil, imgContour)
    
    combinedImage = cv.hconcat([img,imgContour])
    cv.imshow('Before and After',combinedImage)
    
    if cv.waitKey(20) & 0xFF==ord("d"):
        break


#cleanup
capture.release()
cv.destroyAllWindows()

    
