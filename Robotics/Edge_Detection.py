import cv2 as cv
import numpy as np

camera = cv.VideoCapture("0") #limelight url

while True:
    ret, frame = camera.read()
    
    if not ret:
        print("can't read camera") 
        break  

    cv.imshow('camera', frame)

    laplacian = cv.Laplacian(frame, cv.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    cv.imshow('laplacian', laplacian)

    edges = cv.Canny(frame, 100, 100)
    cv.imshow('canny', edges)

    if cv.waitKey(5) & 0xFF == ord('x'):
        break

camera.release()
cv.destroyAllWindows()
