import cv2
import math
from ultralytics import YOLO


# ============================================================
# SIH DRONE - INTEGRATED AI DISASTER DETECTION
# ============================================================

print("=" * 60)
print("        SIH DRONE - INTEGRATED AI SYSTEM")
print("=" * 60)


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
# COCO CLASS IDs WE WANT
# ============================================================

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
# MAIN LOOP
# ============================================================

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break


    # Make a copy for displaying detections
    display = frame.copy()


    # ========================================================
    # 1. PERSON + VEHICLE DETECTION
    # ========================================================

    object_results = object_model(
        frame,
        conf=0.45,
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


            # Person
            if class_id == 0:

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


            # Vehicles / obstacles
            else:

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
        conf=0.40,
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

            elif class_id == 1:
                label = "FIRE"

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
        conf=0.40,
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
            
            if angle < 45:

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
                        "POSSIBLE VICTIM",
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )


    # ========================================================
    # SYSTEM TITLE
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
    # DISPLAY
    # ========================================================

    cv2.imshow(
        "SIH Drone - Integrated Detection",
        display
    )


    # ========================================================
    # QUIT
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

camera.release()
cv2.destroyAllWindows()

print("Integrated detection stopped.")
