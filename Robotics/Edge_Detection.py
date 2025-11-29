import cv2
import numpy as np

# Temporal smoothing variables
prev_center = None
prev_radius = None
smoothing_factor = 0.4  # Reduced for less lag, more responsiveness

def runPipeline(image):
    global prev_center, prev_radius
    
    # 1. Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Adaptive Thresholding - creates high contrast edges
    # Larger block size helps with distant objects
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 2)
    
    # 4. Moderate Morphological Closing - fill small gaps but keep shape
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # 5. Blur the binary image slightly for Hough
    closed_blurred = cv2.GaussianBlur(closed, (9, 9), 2)
    
    # 6. Hough Circle Transform on the processed image
    rows = closed_blurred.shape[0]
    circles = cv2.HoughCircles(closed_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=rows/8,
                               param1=50, param2=26,  # Higher threshold for stability
                               minRadius=8, maxRadius=200)
    
    ball_center = None
    ball_radius = None
    
    output_image = image.copy()

    if circles is not None:
        # Filter circles if we have previous detection
        if prev_center is not None:
            # Find circle closest to previous position
            valid_circles = []
            for circle in circles[0, :]:
                cx, cy, r = circle
                dist = np.sqrt((cx - prev_center[0])**2 + (cy - prev_center[1])**2)
                # Only consider circles within reasonable distance from previous
                if dist < 80:  # Tighter filter to prevent jumping (was 100)
                    valid_circles.append(circle)
            
            if valid_circles:
                # Choose largest valid circle
                largest_circle = max(valid_circles, key=lambda c: c[2])
            else:
                # No valid circles near previous, take largest overall
                largest_circle = max(circles[0, :], key=lambda c: c[2])
        else:
            # No previous detection, just take largest
            largest_circle = max(circles[0, :], key=lambda c: c[2])
        
        circles = np.uint16(np.around(circles))
        center = (int(largest_circle[0]), int(largest_circle[1]))
        radius = int(largest_circle[2])
        
        # === QUALITY CHECKS - Validate this is actually a ball ===
        is_valid_ball = True
        
        # Check 1: Reasonable size (not too small, not too big)
        # Raised minimum to 10 for stricter filtering
        if radius < 10 or radius > 150:
            is_valid_ball = False
        
        # Check 2: Verify circularity by checking the actual contour
        if is_valid_ball:
            # Create a mask of the detected circle region
            mask = np.zeros(closed.shape, dtype=np.uint8)
            cv2.circle(mask, center, radius, 255, -1)
            
            # Find contours in the masked region
            masked_region = cv2.bitwise_and(closed, closed, mask=mask)
            contours, _ = cv2.findContours(masked_region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Get the largest contour in this region
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                perimeter = cv2.arcLength(largest_contour, True)
                
                if perimeter > 0:
                    # Calculate circularity: 4π * area / perimeter²
                    # Perfect circle = 1.0, stricter threshold for better filtering
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    
                    if circularity < 0.65:  # Stricter - must be quite round
                        is_valid_ball = False
                    
                    # Check 3: Area should be reasonable compared to circle area
                    expected_area = np.pi * radius * radius
                    area_ratio = area / expected_area if expected_area > 0 else 0
                    
                    if area_ratio < 0.5:  # Too little fill
                        is_valid_ball = False
        
        # Only accept detection if it passes all quality checks
        if is_valid_ball:
            # Temporal smoothing - blend with previous detection
            if prev_center is not None and prev_radius is not None:
                center = (
                    int(smoothing_factor * prev_center[0] + (1 - smoothing_factor) * center[0]),
                    int(smoothing_factor * prev_center[1] + (1 - smoothing_factor) * center[1])
                )
                radius = int(smoothing_factor * prev_radius + (1 - smoothing_factor) * radius)
            
            ball_center = center
            ball_radius = radius
            
            # Update previous values
            prev_center = center
            prev_radius = radius
            
            # Draw on the output image
            cv2.circle(output_image, center, radius, (0, 255, 0), 3)  # Green circle
            cv2.circle(output_image, center, 2, (0, 255, 255), -1)    # Yellow center
        else:
            # Invalid detection - reset tracking
            prev_center = None
            prev_radius = None

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
