import cv2 as cv
import numpy as np

# Open camera
videoCapture = cv.VideoCapture("http://limelight.local:5800")
prevCircle = None

# Ball tracking settings
TARGET_RADIUS = 150  # Target radius in pixels
TOLERANCE = 20  # Tolerance in pixels

# Stability settings
MAX_JUMP_DISTANCE = 150  # Maximum distance in pixels the ball can "jump" between frames

# Function to calculate distance between two points
dist = lambda x1, y1, x2, y2: (x1 - x2) ** 2 + (y1 - y2) ** 2

while True:
    ret, frame = videoCapture.read()
    if not ret:
        break

    height, width = frame.shape[:2]

    # Convert to grayscale and blur
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (9, 9), 0)

    # Edge detection
    edges = cv.Canny(blurFrame, 30, 100)

    # Close holes in edges
    kernel = np.ones((13, 13), np.uint8)
    closed = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

    # Circle detection
    circles = cv.HoughCircles(
        closed,
        cv.HOUGH_GRADIENT,
        1.2,
        100,
        param1=100,
        param2=30,
        minRadius=30,
        maxRadius=300
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None

        if prevCircle is not None:
            # Choose the circle closest to previous circle
            min_distance = float('inf')
            for i in circles[0, :]:
                d = dist(i[0], i[1], prevCircle[0], prevCircle[1])
                if d < min_distance and d < MAX_JUMP_DISTANCE ** 2:
                    min_distance = d
                    chosen = i
            
            # If no close circle found, choose the largest one
            if chosen is None:
                chosen = max(circles[0, :], key=lambda c: c[2])
        else:
            # If no previous circle, choose the largest (probably closest ball)
            chosen = max(circles[0, :], key=lambda c: c[2])

        # Draw the chosen circle on frame
        cv.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
        cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
        
        prevCircle = chosen

    # Display image with circles
    cv.imshow("circle", frame)

    if cv.waitKey(1) & 0xFF == ord('x'):
        break

videoCapture.release()
cv.destroyAllWindows()