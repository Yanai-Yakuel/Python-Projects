import cv2
import numpy as np

class BallDetector:
    def __init__(self, debug=False):
        self.prev_center = None
        self.prev_radius = None
        self.smoothing_factor = 0.4
        self.debug = debug
        # CLAHE setup for better contrast in changing light
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def reset_tracking(self):
        self.prev_center = None
        self.prev_radius = None

    def process_frame(self, image):
        # 1. Convert to Grayscale & Enhance Contrast
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_enhanced = self.clahe.apply(gray) # Better response to shadows
        
        # 2. Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(gray_enhanced, (9, 9), 2)
        
        # 3. Hough Circles
        rows = blurred.shape[0]
        # param1: Higher threshold for Canny edge detection
        # param2: Accumulator threshold for circle centers (smaller = more false circles)
        circles = cv2.HoughCircles(
            blurred, 
            cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=rows/4,
            param1=100, 
            param2=30,
            minRadius=20, 
            maxRadius=200
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
                
                # Basic sanity check
                if r < 10 or r > 200: 
                    continue
                    
                score = 0
                
                # Tracking Logic
                if self.prev_center is not None:
                    # Distance from previous frame
                    dist = np.sqrt((cx - self.prev_center[0])**2 + (cy - self.prev_center[1])**2)
                    size_diff = abs(int(r) - int(self.prev_radius))
                    
                    # Weight distance heavily
                    score = dist + (size_diff * 3)
                    
                    # Gate: If too far or size changed drastically, penalize heavily
                    if dist > 100 or size_diff > 50:
                        score += 1000 
                else:
                    # If not tracking, prefer larger circles (assuming ball is prominent)
                    score = 1000 - r 
                
                candidates.append((score, c))
            
            # Pick best candidate
            if candidates:
                candidates.sort(key=lambda x: x[0]) # Lowest score is best
                best_circle = candidates[0][1]
                
                # Unwrap
                target_center = (best_circle[0], best_circle[1])
                target_radius = best_circle[2]
                
                # Implement Temporal Smoothing
                if self.prev_center is not None:
                     # Calculate distance again for specific check
                    dist = np.sqrt((target_center[0] - self.prev_center[0])**2 + 
                                 (target_center[1] - self.prev_center[1])**2)
                    
                    if dist < 120: # Valid movement range
                        target_center = (
                            int(self.smoothing_factor * self.prev_center[0] + (1 - self.smoothing_factor) * target_center[0]),
                            int(self.smoothing_factor * self.prev_center[1] + (1 - self.smoothing_factor) * target_center[1])
                        )
                        target_radius = int(self.smoothing_factor * self.prev_radius + (1 - self.smoothing_factor) * target_radius)
                    else:
                        # Reset if jumped too far (teleportation is physically impossible)
                        self.reset_tracking()

                current_center = target_center
                current_radius = target_radius
                
                self.prev_center = current_center
                self.prev_radius = current_radius

                # Visualization
                cv2.circle(output_image, current_center, current_radius, (0, 255, 0), 3)
                cv2.circle(output_image, current_center, 2, (0, 255, 255), -1)
            else:
                self.reset_tracking()
        else:
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
