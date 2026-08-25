import cv2
import math
from collections import defaultdict
from ultralytics import YOLO


# ============================================================
# SIH DRONE - ENHANCED VICTIM DETECTION
# YOLO Pose + Body Orientation + Temporal Confirmation
# ============================================================

print("Starting SIH Drone Enhanced Victim Detection...")


# ------------------------------------------------------------
# 1. LOAD YOLO POSE MODEL
# ------------------------------------------------------------

model = YOLO("yolo11n-pose.pt")


# ------------------------------------------------------------
# 2. OPEN CAMERA
# ------------------------------------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

print("Camera started successfully.")
print("Press Q to stop.")


# ------------------------------------------------------------
# 3. SETTINGS
# ------------------------------------------------------------

PERSON_CONFIDENCE = 0.45
KEYPOINT_CONFIDENCE = 0.35

# Number of consecutive frames required before
# declaring a possible victim
VICTIM_CONFIRM_FRAMES = 15

# Store confirmation count for detected people
victim_counter = defaultdict(int)


# ------------------------------------------------------------
# 4. HELPER FUNCTIONS
# ------------------------------------------------------------

def calculate_angle(x1, y1, x2, y2):
    """
    Calculate angle of a line relative to horizontal.
    0°   = horizontal
    90°  = vertical
    """

    dx = x2 - x1
    dy = y2 - y1

    angle = math.degrees(math.atan2(dy, dx))

    # Convert to 0-180 range
    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


def point_valid(point, confidence):
    """
    Check whether a pose keypoint is reliable.
    """

    return confidence >= KEYPOINT_CONFIDENCE


# ------------------------------------------------------------
# 5. MAIN LOOP
# ------------------------------------------------------------

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break


    # --------------------------------------------------------
    # RUN YOLO POSE DETECTION
    # --------------------------------------------------------

    results = model(
        frame,
        verbose=False,
        conf=PERSON_CONFIDENCE
    )


    current_people = set()


    # --------------------------------------------------------
    # PROCESS DETECTIONS
    # --------------------------------------------------------

    for result in results:

        if result.boxes is None:
            continue

        if result.keypoints is None:
            continue


        boxes = result.boxes
        keypoints = result.keypoints


        for i in range(len(boxes)):

            # ------------------------------------------------
            # CLASS CHECK
            # ------------------------------------------------
            # COCO class 0 = person
            #
            # This prevents animals such as dogs/cats/cows
            # from being treated as victims.
            # ------------------------------------------------

            class_id = int(boxes.cls[i].item())

            if class_id != 0:
                continue


            confidence = float(boxes.conf[i].item())

            if confidence < PERSON_CONFIDENCE:
                continue


            # ------------------------------------------------
            # BOUNDING BOX
            # ------------------------------------------------

            x1, y1, x2, y2 = map(
                int,
                boxes.xyxy[i].tolist()
            )

            width = x2 - x1
            height = y2 - y1


            if width <= 0 or height <= 0:
                continue


            # ------------------------------------------------
            # GET POSE KEYPOINTS
            # ------------------------------------------------

            kp = keypoints.xy[i].cpu().numpy()
            kp_conf = keypoints.conf[i].cpu().numpy()


            # COCO KEYPOINT INDEXES
            #
            # 5  = left shoulder
            # 6  = right shoulder
            # 11 = left hip
            # 12 = right hip
            # 13 = left knee
            # 14 = right knee
            # 15 = left ankle
            # 16 = right ankle
            # ------------------------------------------------


            # ------------------------------------------------
            # CHECK SHOULDERS + HIPS
            # ------------------------------------------------

            required_points = [5, 6, 11, 12]

            if not all(
                point_valid(kp[p], kp_conf[p])
                for p in required_points
            ):
                # Not enough reliable pose information
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 165, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"PERSON {confidence:.2f}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 165, 255),
                    2
                )

                continue


            # ------------------------------------------------
            # SHOULDER CENTER
            # ------------------------------------------------

            left_shoulder = kp[5]
            right_shoulder = kp[6]

            shoulder_x = (
                left_shoulder[0] +
                right_shoulder[0]
            ) / 2

            shoulder_y = (
                left_shoulder[1] +
                right_shoulder[1]
            ) / 2


            # ------------------------------------------------
            # HIP CENTER
            # ------------------------------------------------

            left_hip = kp[11]
            right_hip = kp[12]

            hip_x = (
                left_hip[0] +
                right_hip[0]
            ) / 2

            hip_y = (
                left_hip[1] +
                right_hip[1]
            ) / 2


            # ------------------------------------------------
            # BODY ORIENTATION
            # ------------------------------------------------

            body_angle = calculate_angle(
                shoulder_x,
                shoulder_y,
                hip_x,
                hip_y
            )


            # Normalize angle so:
            #
            # ~0°   = body is horizontal
            # ~90°  = body is vertical
            #

            if body_angle > 90:
                body_angle = 180 - body_angle


            # ------------------------------------------------
            # BODY ASPECT RATIO
            # ------------------------------------------------

            aspect_ratio = width / max(height, 1)


            # ------------------------------------------------
            # CHECK LOWER BODY
            # ------------------------------------------------

            lower_body_visible = False

            ankle_points = [15, 16]

            for p in ankle_points:

                if kp_conf[p] >= KEYPOINT_CONFIDENCE:
                    lower_body_visible = True
                    break


            # ------------------------------------------------
            # DETERMINE BODY POSITION
            # ------------------------------------------------

            is_horizontal_body = body_angle < 45

            is_wide_body = aspect_ratio > 1.15


            # ------------------------------------------------
            # POSSIBLE LYING CONDITION
            # ------------------------------------------------

            possible_lying = (
                is_horizontal_body
                and is_wide_body
            )


            # ------------------------------------------------
            # PERSON ID
            #
            # For this prototype we use the detection index.
            # Later we can replace this with YOLO tracking.
            # ------------------------------------------------

            person_id = i

            current_people.add(person_id)


            # ------------------------------------------------
            # TEMPORAL CONFIRMATION
            # ------------------------------------------------

            if possible_lying:

                victim_counter[person_id] += 1

            else:

                # Slowly reset instead of immediately forgetting
                victim_counter[person_id] = max(
                    0,
                    victim_counter[person_id] - 2
                )


            # ------------------------------------------------
            # FINAL VICTIM DECISION
            # ------------------------------------------------

            confirmed_victim = (
                victim_counter[person_id]
                >= VICTIM_CONFIRM_FRAMES
            )


            # ------------------------------------------------
            # DRAW BODY ORIENTATION LINE
            # ------------------------------------------------

            cv2.line(
                frame,
                (int(shoulder_x), int(shoulder_y)),
                (int(hip_x), int(hip_y)),
                (255, 0, 255),
                3
            )


            # ------------------------------------------------
            # DRAW KEYPOINTS
            # ------------------------------------------------

            important_points = [
                5, 6, 11, 12,
                13, 14, 15, 16
            ]

            for p in important_points:

                if kp_conf[p] >= KEYPOINT_CONFIDENCE:

                    px = int(kp[p][0])
                    py = int(kp[p][1])

                    cv2.circle(
                        frame,
                        (px, py),
                        5,
                        (0, 255, 0),
                        -1
                    )


            # ------------------------------------------------
            # DISPLAY STATUS
            # ------------------------------------------------

            if confirmed_victim:

                box_color = (0, 0, 255)

                label = (
                    f"POSSIBLE VICTIM "
                    f"{confidence:.2f}"
                )

            elif possible_lying:

                box_color = (0, 165, 255)

                label = (
                    f"LYING? "
                    f"{confidence:.2f}"
                )

            else:

                box_color = (0, 255, 0)

                label = (
                    f"PERSON "
                    f"{confidence:.2f}"
                )


            # ------------------------------------------------
            # DRAW PERSON BOX
            # ------------------------------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                box_color,
                3
            )


            # ------------------------------------------------
            # DISPLAY LABEL
            # ------------------------------------------------

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 12, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                box_color,
                2
            )


            # ------------------------------------------------
            # DISPLAY BODY ANGLE
            # ------------------------------------------------

            cv2.putText(
                frame,
                f"Body angle: {body_angle:.1f} deg",
                (x1, y2 + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )


            # ------------------------------------------------
            # DISPLAY CONFIRMATION PROGRESS
            # ------------------------------------------------

            if possible_lying and not confirmed_victim:

                cv2.putText(
                    frame,
                    f"Confirming: "
                    f"{victim_counter[person_id]}"
                    f"/{VICTIM_CONFIRM_FRAMES}",
                    (x1, y2 + 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 165, 255),
                    2
                )


    # --------------------------------------------------------
    # CLEAN OLD PERSON COUNTERS
    # --------------------------------------------------------

    old_ids = set(victim_counter.keys()) - current_people

    for old_id in old_ids:

        victim_counter[old_id] = max(
            0,
            victim_counter[old_id] - 1
        )

        if victim_counter[old_id] == 0:

            del victim_counter[old_id]


    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    cv2.putText(
        frame,
        "SIH DRONE - VICTIM DETECTION",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        "Q = Stop",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # SHOW CAMERA
    # --------------------------------------------------------

    cv2.imshow(
        "SIH Drone - Enhanced Victim Detection",
        frame
    )


    # --------------------------------------------------------
    # QUIT
    # --------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


# ------------------------------------------------------------
# CLEANUP
# ------------------------------------------------------------

camera.release()
cv2.destroyAllWindows()

print("Victim detection stopped.")