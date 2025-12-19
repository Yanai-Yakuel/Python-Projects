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

        # FTC 2026 - סלחנות מקסימלית לרעש מעל הכדור
        self.arc_fraction_thresh_min = 0.10   # 10% היקף מספיק!
        self.arc_fraction_half = 0.45
        self.arc_fraction_full = 0.7
        self.occlusion_grace_frames = 12      # 12 פריימים נעילה

    def reset_tracking(self):
        self.prev_center = None
        self.prev_radius = None

    # **שדרוג קריטי: מתעלם מרעש בחלק העליון של הכדור!**
    def _circle_edge_fraction(self, gray_img, center, radius, samples=90):
        cx, cy = center
        h, w = gray_img.shape[:2]

        # Canny סלחני יותר לזירה FTC
        edges = cv2.Canny(gray_img, 60, 140)

        hits = 0
        total = 0

        for i in range(samples):
            theta = 2.0 * np.pi * i / samples
            x = int(cx + radius * np.cos(theta))
            y = int(cy + radius * np.sin(theta))

            if x <= 2 or x >= w - 3 or y <= 2 or y >= h - 3:
                continue

            # **הפתרון לרעש מעל הכדור: מתעלמים מ-30% העליון!**
            if y < cy - radius * 0.3:  # דלג על חלק עליון (רעש!)
                continue

            total += 1
            roi = edges[y-2:y+4, x-2:x+4]  # ROI גדול יותר לקצוות
            if np.any(roi > 0):
                hits += 1

        if total == 0:
            return 0.0

        return hits / float(total)

    def process_frame(self, image):
        self.frame_count += 1
        
        # 1. Convert to Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. CLAHE for better contrast in changing light
        gray_enhanced = self.clahe.apply(gray)
        
        # 3. Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(gray_enhanced, (9, 9), 2)
        
        # 3b. Morphological operations to remove wall texture noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        blurred = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
        blurred = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)

        # 4. Adaptive Hough Circles
        rows = blurred.shape[0]
        
        if self.prev_center is None:
            param1_threshold = 95
            param2_threshold = 25
            min_radius = 10
            max_radius = 200
        else:
            expected_radius = self.prev_radius
            param1_threshold = 110
            param2_threshold = 32
            min_radius = max(8, int(expected_radius * 0.4))
            max_radius = min(200, int(expected_radius * 2.5))

        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=max(rows // 6, 50),
            param1=param1_threshold,
            param2=param2_threshold,
            minRadius=min_radius,
            maxRadius=max_radius
        )

        output_image = image.copy()
        current_center = None
        current_radius = None
        current_arc_fraction = 0.0

        if circles is not None:
            circles = np.uint16(np.around(circles))
            candidates = []

            for c in circles[0, :]:
                cx, cy, r = c

                if r < 12 or r > 180:
                    continue

                if cx - r < 5 or cy - r < 5 or cx + r >= image.shape[1] - 5 or cy + r >= image.shape[0] - 5:
                    continue

                score = float('inf')

                if self.prev_center is not None:
                    dist = np.sqrt((cx - self.prev_center[0]) ** 2 + (cy - self.prev_center[1]) ** 2)
                    size_diff = abs(int(r) - int(self.prev_radius))

                    if dist > 60 or size_diff > 15:
                        continue

                    score = dist * 3 + size_diff * 5
                else:
                    center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
                    center_dist = np.sqrt((cx - center_x) ** 2 + (cy - center_y) ** 2)
                    score = center_dist

                candidates.append((score, c))

            if candidates:
                candidates.sort(key=lambda x: x[0])
                best_circle = candidates[0][1]

                target_center = (int(best_circle[0]), int(best_circle[1]))
                target_radius = int(best_circle[2])

                current_arc_fraction = self._circle_edge_fraction(blurred, target_center, target_radius)

                # **לוגיקה משופרת לרעש מעל הכדור**
                if current_arc_fraction < self.arc_fraction_thresh_min:
                    # כיסוי/רעש מעל - נשארים נעולים!
                    if self.prev_center is not None:
                        self.lost_frames += 1
                        if self.lost_frames <= self.occlusion_grace_frames:
                            current_center = self.prev_center
                            current_radius = self.prev_radius
                            color = (255, 0, 255)  # סגול = נעול למרות רעש
                            cv2.circle(output_image, current_center, current_radius, color, 3)
                            cv2.circle(output_image, current_center, 2, (255, 0, 255), -1)
                        else:
                            self.reset_tracking()
                    else:
                        self.lost_frames += 1
                        if self.lost_frames > 20:
                            self.reset_tracking()
                else:
                    # זיהוי טוב - smoothing
                    self.lost_frames = 0

                    if self.prev_center is not None:
                        vx = target_center[0] - self.prev_center[0]
                        vy = target_center[1] - self.prev_center[1]

                        target_center = (
                            int(self.smoothing_factor * self.prev_center[0] +
                                (1 - self.smoothing_factor) * target_center[0]),
                            int(self.smoothing_factor * self.prev_center[1] +
                                (1 - self.smoothing_factor) * target_center[1])
                        )
                        target_radius = int(
                            self.smoothing_factor * self.prev_radius +
                            (1 - self.smoothing_factor) * target_radius
                        )

                        self.prev_velocity = (vx, vy)

                    current_center = target_center
                    current_radius = target_radius
                    self.prev_center = current_center
                    self.prev_radius = current_radius

                    # Visualization
                    if current_arc_fraction >= self.arc_fraction_full:
                        color = (0, 255, 0)
                    elif current_arc_fraction >= self.arc_fraction_half:
                        color = (0, 255, 255)
                    else:
                        color = (0, 128, 255)

                    cv2.circle(output_image, current_center, current_radius, color, 3)
                    cv2.circle(output_image, current_center, 2, (0, 0, 255), -1)

                    if self.debug:
                        txt = f"arc={current_arc_fraction:.2f}"
                        cv2.putText(output_image, txt, (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                        cv2.putText(output_image, f"lost={self.lost_frames}", (10, 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
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
            llpython[3] = float(current_arc_fraction)
            llpython[4] = float(self.lost_frames)  # מצב כיסוי

        return [], output_image, llpython


# --- Wrapper for Limelight (Pipeline Interface) ---
detector = BallDetector(debug=True)


def runPipeline(image, llrobot=None):
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
            print(
                f"Detected: x={llpython[0]:.1f}, y={llpython[1]:.1f}, "
                f"r={llpython[2]:.1f}, arc={llpython[3]:.2f}, lost={llpython[4]:.0f}"
            )

        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()
