import cv2
import numpy as np

prev_edges = None  # לשימוש ב-Weighted Previous Frame

def runPipeline(image):
    # 1. Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Gaussian Blur (Standard)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # 3. Hough Circle Transform (Standard)
    # Reverted to the version that worked for close range (20-30cm)
    rows = blurred.shape[0]
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=rows/8,
                               param1=100, param2=30,
                               minRadius=20, maxRadius=200)
    
    ball_center = None
    ball_radius = None
    
    output_image = image.copy()

    if circles is not None:
        circles = np.uint16(np.around(circles))
        # Find the largest circle
        largest_circle = max(circles[0, :], key=lambda c: c[2])
        
        center = (largest_circle[0], largest_circle[1])
        radius = largest_circle[2]
        
        ball_center = center
        ball_radius = int(radius)
        
        # Draw on the output image
        cv2.circle(output_image, center, 1, (0, 100, 100), 3)
        cv2.circle(output_image, center, radius, (255, 0, 255), 3)

    contours_return = [] 
    llpython = [0] * 8
    
    if ball_center is not None:
        llpython[0] = ball_center[0]
        llpython[1] = ball_center[1]
        llpython[2] = ball_radius

    return contours_return, output_image, llpython


# --- MAIN LOOP ---
if __name__ == "__main__":
    limelight_url = "http://limelight.local:5800/stream.mjpg"
    cap = cv2.VideoCapture(limelight_url)

    if not cap.isOpened():
        print("Could not connect to Limelight, switching to local camera...")
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Failed to open any camera.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        contours, output_image, llpython = runPipeline(frame)

        cv2.imshow("Limelight Output", output_image)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()
