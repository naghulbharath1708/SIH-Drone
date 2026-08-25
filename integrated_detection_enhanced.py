import cv2
import math
import time
from datetime import datetime
from ultralytics import YOLO


# ============================================================
# SIH DRONE - INTEGRATED AI DISASTER DETECTION
# ENHANCED DEMONSTRATION VERSION
# ============================================================

print("=" * 70)
print("        SIH DRONE - INTEGRATED AI DISASTER DETECTION")
print("        SEARCH + RESCUE | HAZARD AWARENESS | LIVE STATUS")
print("=" * 70)


# ============================================================
# 1. LOAD AI MODELS
# ============================================================

print("Loading AI models...")

# Normal YOLO model
# Used for:
# Person, Bicycle, Car, Motorcycle, Bus, Truck
object_model = YOLO("yolo11n.pt")

# Pose model
# Used for identifying possible fallen / lying victims
pose_model = YOLO("yolo11n-pose.pt")

# Fire + Smoke model
# 0 = smoke, 1 = fire
fire_model = YOLO("fire_smoke.pt")

print("All AI models loaded successfully!")


# ============================================================
# 2. CAMERA
# ============================================================

print("Starting camera...")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

print("Camera opened successfully!")
print("Press Q to stop.")


# ============================================================
# 3. TARGET CLASSES
# ============================================================

# COCO class IDs:
# 0 = person
# 1 = bicycle
# 2 = car
# 3 = motorcycle
# 5 = bus
# 7 = truck

TARGET_CLASSES = {
    0: "PERSON",
    1: "BICYCLE",
    2: "CAR",
    3: "MOTORCYCLE",
    5: "BUS",
    7: "TRUCK"
}


# ============================================================
# 4. SYSTEM SETTINGS
# ============================================================

OBJECT_CONFIDENCE = 0.45
FIRE_CONFIDENCE = 0.40
POSE_CONFIDENCE = 0.40

# Victim angle threshold:
# Smaller torso angle means a more horizontal body.
VICTIM_ANGLE_THRESHOLD = 45

# Counters are reset for every frame.
person_count = 0
vehicle_count = 0
fire_count = 0
smoke_count = 0
victim_count = 0

# FPS calculation
previous_time = time.time()
fps = 0.0

# Used to avoid printing the same alert continuously.
last_alert_time = 0
ALERT_COOLDOWN = 3.0


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def draw_status_panel(
    image,
    person_count,
    vehicle_count,
    fire_count,
    smoke_count,
    victim_count,
    fps_value,
    threat_level
):
    """Draw the live mission dashboard on the video frame."""

    panel_x1 = 10
    panel_y1 = 50
    panel_x2 = 330
    panel_y2 = 245

    # Semi-transparent black panel
    overlay = image.copy()

    cv2.rectangle(
        overlay,
        (panel_x1, panel_y1),
        (panel_x2, panel_y2),
        (0, 0, 0),
        -1
    )

    image[:] = cv2.addWeighted(
        overlay,
        0.60,
        image,
        0.40,
        0
    )

    # Dashboard title
    cv2.putText(
        image,
        "MISSION DASHBOARD",
        (25, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        image,
        f"PERSONS       : {person_count}",
        (25, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )

    cv2.putText(
        image,
        f"VEHICLES      : {vehicle_count}",
        (25, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )

    cv2.putText(
        image,
        f"FIRE          : {fire_count}",
        (25, 155),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )

    cv2.putText(
        image,
        f"SMOKE         : {smoke_count}",
        (25, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )

    cv2.putText(
        image,
        f"POSSIBLE VICT.: {victim_count}",
        (25, 205),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )

    cv2.putText(
        image,
        f"FPS           : {fps_value:.1f}",
        (25, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )

    # Threat level
    threat_text = f"THREAT LEVEL: {threat_level}"

    cv2.putText(
        image,
        threat_text,
        (350, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


def calculate_threat_level(
    fire_count,
    smoke_count,
    victim_count
):
    """
    Calculate a simple demonstration threat level.

    HIGH:
        Fire detected OR victim detected with fire/smoke.

    MEDIUM:
        Smoke detected OR possible victim detected.

    LOW:
        People/objects detected but no direct hazard.

    CLEAR:
        No relevant detection.
    """

    if fire_count > 0:
        return "HIGH"

    if victim_count > 0 and smoke_count > 0:
        return "HIGH"

    if smoke_count > 0 or victim_count > 0:
        return "MEDIUM"

    return "CLEAR"


def print_event_alert(
    fire_count,
    smoke_count,
    victim_count,
    threat_level
):
    """Print a readable event alert in the terminal."""

    global last_alert_time

    current_time = time.time()

    if current_time - last_alert_time < ALERT_COOLDOWN:
        return

    alert_message = None

    if fire_count > 0:
        alert_message = "FIRE DETECTED - IMMEDIATE HAZARD"

    elif victim_count > 0 and smoke_count > 0:
        alert_message = "POSSIBLE VICTIM + SMOKE DETECTED"

    elif victim_count > 0:
        alert_message = "POSSIBLE VICTIM DETECTED"

    elif smoke_count > 0:
        alert_message = "SMOKE DETECTED - CHECK AREA"

    if alert_message is not None:
        timestamp = datetime.now().strftime("%H:%M:%S")

        print()
        print("!" * 60)
        print(f"[{timestamp}] ALERT: {alert_message}")
        print(f"THREAT LEVEL: {threat_level}")
        print("!" * 60)
        print()

        last_alert_time = current_time


# ============================================================
# 6. MAIN LOOP
# ============================================================

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break

    # --------------------------------------------------------
    # FPS
    # --------------------------------------------------------

    current_time = time.time()
    time_difference = current_time - previous_time

    if time_difference > 0:
        fps = 1.0 / time_difference

    previous_time = current_time


    # --------------------------------------------------------
    # Reset per-frame counters
    # --------------------------------------------------------

    person_count = 0
    vehicle_count = 0
    fire_count = 0
    smoke_count = 0
    victim_count = 0


    # Make a copy for displaying detections
    display = frame.copy()


    # ========================================================
    # 1. PERSON + VEHICLE DETECTION
    # ========================================================

    object_results = object_model(
        frame,
        conf=OBJECT_CONFIDENCE,
        classes=list(TARGET_CLASSES.keys()),
        verbose=False
    )


    for result in object_results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            if class_id not in TARGET_CLASSES:
                continue

            label = TARGET_CLASSES[class_id]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )


            # ------------------------------------------------
            # Person
            # ------------------------------------------------

            if class_id == 0:

                person_count += 1

                cv2.rectangle(
                    display,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 0),
                    2
                )

                cv2.putText(
                    display,
                    f"PERSON {confidence:.2f}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2
                )


            # ------------------------------------------------
            # Vehicles / obstacles
            # ------------------------------------------------

            else:

                vehicle_count += 1

                cv2.rectangle(
                    display,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    display,
                    f"{label} {confidence:.2f}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )


    # ========================================================
    # 2. FIRE + SMOKE DETECTION
    # ========================================================

    fire_results = fire_model(
        frame,
        conf=FIRE_CONFIDENCE,
        verbose=False
    )


    for result in fire_results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            # Our fire_smoke model:
            # 0 = smoke
            # 1 = fire

            if class_id == 0:
                label = "SMOKE"
                smoke_count += 1

            elif class_id == 1:
                label = "FIRE"
                fire_count += 1

            else:
                continue


            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )


            cv2.rectangle(
                display,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )


            cv2.putText(
                display,
                f"{label} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 0, 255),
                2
            )


    # ========================================================
    # 3. VICTIM / POSE DETECTION
    # ========================================================

    pose_results = pose_model(
        frame,
        conf=POSE_CONFIDENCE,
        verbose=False
    )


    for result in pose_results:

        if result.keypoints is None:
            continue

        if result.keypoints.xy is None:
            continue


        keypoints = result.keypoints.xy

        if len(keypoints) == 0:
            continue


        # Process every detected person
        for person_index in range(len(keypoints)):

            points = keypoints[person_index]


            # Need at least the important body points
            if len(points) < 17:
                continue


            # COCO pose keypoints:
            #
            # 5  = left shoulder
            # 6  = right shoulder
            # 11 = left hip
            # 12 = right hip

            left_shoulder = points[5]
            right_shoulder = points[6]

            left_hip = points[11]
            right_hip = points[12]


            # Check that coordinates exist
            if (
                left_shoulder[0] == 0
                or right_shoulder[0] == 0
                or left_hip[0] == 0
                or right_hip[0] == 0
            ):
                continue


            # Calculate shoulder centre
            shoulder_x = (
                float(left_shoulder[0])
                + float(right_shoulder[0])
            ) / 2

            shoulder_y = (
                float(left_shoulder[1])
                + float(right_shoulder[1])
            ) / 2


            # Calculate hip centre
            hip_x = (
                float(left_hip[0])
                + float(right_hip[0])
            ) / 2

            hip_y = (
                float(left_hip[1])
                + float(right_hip[1])
            ) / 2


            # Body direction
            dx = hip_x - shoulder_x
            dy = hip_y - shoulder_y


            angle = abs(
                math.degrees(
                    math.atan2(dy, dx)
                )
            )


            # Normalize angle
            if angle > 90:
                angle = 180 - angle


            # =================================================
            # POSSIBLE VICTIM CONDITION
            # =================================================

            # A standing person's torso is approximately
            # vertical.
            #
            # A lying person's torso becomes much more
            # horizontal.
            #
            # This is a basic victim-detection condition.

            if angle < VICTIM_ANGLE_THRESHOLD:

                # Estimate victim bounding area
                xs = [
                    int(float(p[0]))
                    for p in points
                    if float(p[0]) > 0
                ]

                ys = [
                    int(float(p[1]))
                    for p in points
                    if float(p[1]) > 0
                ]


                if len(xs) > 0 and len(ys) > 0:

                    victim_count += 1

                    x1 = min(xs)
                    y1 = min(ys)
                    x2 = max(xs)
                    y2 = max(ys)


                    cv2.rectangle(
                        display,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        3
                    )


                    cv2.putText(
                        display,
                        f"POSSIBLE VICTIM {angle:.0f}deg",
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (0, 255, 0),
                        2
                    )


    # ========================================================
    # 4. THREAT ASSESSMENT
    # ========================================================

    threat_level = calculate_threat_level(
        fire_count,
        smoke_count,
        victim_count
    )


    # Print important events to terminal
    print_event_alert(
        fire_count,
        smoke_count,
        victim_count,
        threat_level
    )


    # ========================================================
    # 5. SYSTEM TITLE
    # ========================================================

    cv2.putText(
        display,
        "SIH DRONE - AI DISASTER DETECTION",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # ========================================================
    # 6. LIVE MISSION DASHBOARD
    # ========================================================

    draw_status_panel(
        display,
        person_count,
        vehicle_count,
        fire_count,
        smoke_count,
        victim_count,
        fps,
        threat_level
    )


    # ========================================================
    # 7. STATUS MESSAGE
    # ========================================================

    if threat_level == "HIGH":
        status_message = "!!! EMERGENCY - RESPONDER CAUTION !!!"

    elif threat_level == "MEDIUM":
        status_message = "CAUTION - POTENTIAL HAZARD"

    elif threat_level == "LOW":
        status_message = "AREA MONITORING"

    else:
        status_message = "AREA STATUS: CLEAR"


    cv2.putText(
        display,
        status_message,
        (20, display.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


    # ========================================================
    # 8. CURRENT TIME
    # ========================================================

    timestamp = datetime.now().strftime("%H:%M:%S")

    cv2.putText(
        display,
        timestamp,
        (display.shape[1] - 100, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )


    # ========================================================
    # 9. DISPLAY
    # ========================================================

    cv2.imshow(
        "SIH Drone - Integrated Detection",
        display
    )


    # ========================================================
    # 10. QUIT
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

camera.release()
cv2.destroyAllWindows()

print("=" * 60)
print("Integrated detection stopped.")
print("SIH Drone system shutdown complete.")
print("=" * 60)
