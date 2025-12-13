import cv2
import numpy as np

class BallDetector:
    def __init__(self, debug=False):
        self.prev_center = None
        self.prev_radius = None
        self.prev_velocity = (0, 0)  # Track velocity for prediction
        self.smoothing_factor = 0.75  # Balanced smoothing
        self.debug = debug
        self.frame_count = 0
        self.lost_frames = 0
        # CLAHE setup for better contrast in changing light
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def reset_tracking(self):
        self.prev_center = None
        self.prev_radius = None

    def process_frame(self, image):
        self.frame_count += 1
        
        # 1. Convert to Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. CLAHE for better contrast in close-up and varying lighting
        gray_enhanced = self.clahe.apply(gray)
        
        # 3. Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(gray_enhanced, (9, 9), 2)
        
        # 3b. Morphological operations to remove wall texture noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        blurred = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)  # Fill small holes in ball
        blurred = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)   # Remove small wall noise
        
        # 4. Adaptive Hough Circles - parameters adapt based on tracking state
        rows = blurred.shape[0]
        
        # When we have no previous radius, we don't know ball size, so be more lenient
        # When we know the ball size, use stricter parameters
        if self.prev_center is None:
            # Initialization mode: look for circles broadly - any size
            param1_threshold = 95  # Lower edge threshold to catch balls at any distance
            param2_threshold = 25   # Moderate accumulator threshold
            min_radius = 10  # Allow very small circles (distant ball)
            max_radius = 200  # Allow large circles
        else:
            # Tracking mode: use radius to adapt detection
            expected_radius = self.prev_radius
            # Tighter parameters when tracking
            param1_threshold = 110
            param2_threshold = 32
            # Expand search range based on expected size (allow size changes up to 2x for zoom in/out)
            min_radius = max(8, int(expected_radius * 0.4))
            max_radius = min(200, int(expected_radius * 2.5))
        
        circles = cv2.HoughCircles(
            blurred, 
            cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=max(rows//6, 50),
            param1=param1_threshold,
            param2=param2_threshold,
            minRadius=min_radius, 
            maxRadius=max_radius
        )
        
        output_image = image.copy()
        current_center = None
        current_radius = None
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            candidates = []
            
            # Filter and Score Candidates
            for c in circles[0, :]:
                cx, cy, r = c
                
                # Sanity checks
                if r < 12 or r > 180: 
                    continue
                
                # Boundary check: ball should be mostly visible
                if cx - r < 5 or cy - r < 5 or cx + r >= image.shape[1] - 5 or cy + r >= image.shape[0] - 5:
                    continue
                    
                score = float('inf')
                
                # Scoring based on tracking state - prefer stability and reject hand
                if self.prev_center is not None:
                    dist = np.sqrt((cx - self.prev_center[0])**2 + (cy - self.prev_center[1])**2)
                    size_diff = abs(int(r) - int(self.prev_radius))
                    
                    # VERY STRICT: Keep lock on ball, don't jump around
                    # Limit distance and size change strictly
                    if dist > 60 or size_diff > 15:
                        continue  # Hard reject - likely noise or hand
                    
                    # Score: prefer closest match to previous position (tight lock)
                    score = dist * 3 + size_diff * 5
                else:
                    # When initializing, prefer centered circles only
                    # Don't care about size, just find a circle near center
                    center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
                    center_dist = np.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                    # Simple scoring: prefer centered circles, ignore size
                    score = center_dist
                
                candidates.append((score, c))
            
            # Pick best candidate
            if candidates:
                candidates.sort(key=lambda x: x[0])
                best_circle = candidates[0][1]
                
                target_center = (int(best_circle[0]), int(best_circle[1]))
                target_radius = int(best_circle[2])
                
                # Temporal smoothing - smooth but still responsive
                if self.prev_center is not None:
                    # Calculate velocity
                    vx = target_center[0] - self.prev_center[0]
                    vy = target_center[1] - self.prev_center[1]
                    
                    # Apply low-pass filter for smooth motion
                    target_center = (
                        int(self.smoothing_factor * self.prev_center[0] + (1 - self.smoothing_factor) * target_center[0]),
                        int(self.smoothing_factor * self.prev_center[1] + (1 - self.smoothing_factor) * target_center[1])
                    )
                    target_radius = int(self.smoothing_factor * self.prev_radius + (1 - self.smoothing_factor) * target_radius)
                    
                    self.prev_velocity = (vx, vy)

                current_center = target_center
                current_radius = target_radius
                
                self.prev_center = current_center
                self.prev_radius = current_radius
                self.lost_frames = 0

                # Visualization
                cv2.circle(output_image, current_center, current_radius, (0, 255, 0), 3)
                cv2.circle(output_image, current_center, 2, (0, 255, 255), -1)
            else:
                self.lost_frames += 1
                if self.lost_frames > 20:
                    self.reset_tracking()
        else:
            self.lost_frames += 1
            if self.lost_frames > 20:
                self.reset_tracking()

        # Prepare Limelight Data
        llpython = [0.0] * 8
        if current_center is not None:
            llpython[0] = float(current_center[0])
            llpython[1] = float(current_center[1])
            llpython[2] = float(current_radius)

        return [], output_image, llpython

# --- Wrapper for Limelight (Pipeline Interface) ---
detector = BallDetector()

def runPipeline(image, llrobot=None):
    # Support both signatures (with and without llrobot data)
    return detector.process_frame(image)

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
        
        # Print detected info to console
        if llpython[0] != 0:
            print(f"Detected: x={llpython[0]:.1f}, y={llpython[1]:.1f}, r={llpython[2]:.1f}")

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()