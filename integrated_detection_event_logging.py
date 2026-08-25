import cv2
import math
import time
import csv
import os
from datetime import datetime
from ultralytics import YOLO


# ============================================================
# SIH DRONE - INTEGRATED AI DISASTER DETECTION
# FINAL DASHBOARD + EVENT LOGGING VERSION
# ============================================================


# ============================================================
# 1. EVENT LOGGING SETTINGS
# ============================================================

LOG_FILE = "event_log.csv"

EVENT_COOLDOWN = 5.0

last_logged_events = {}

last_event_text = "SYSTEM READY"

total_events_logged = 0


# ============================================================
# 2. EVENT LOGGER
# ============================================================

def log_event(
    event_type,
    confidence="",
    count="",
    details="",
    threat_level="CLEAR"
):

    global total_events_logged
    global last_event_text

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    file_exists = os.path.exists(LOG_FILE)

    try:

        with open(
            LOG_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "Timestamp",
                    "Event",
                    "Confidence",
                    "Count",
                    "Details",
                    "Threat Level"
                ])

            writer.writerow([
                timestamp,
                event_type,
                confidence,
                count,
                details,
                threat_level
            ])

        total_events_logged += 1

        last_event_text = event_type

        print(
            f"[EVENT LOG] {timestamp} | "
            f"{event_type} | "
            f"Confidence: {confidence} | "
            f"Count: {count} | "
            f"Threat: {threat_level}"
        )

    except Exception as error:

        print(
            f"[EVENT LOG ERROR] {error}"
        )


def should_log_event(event_name):

    current_time = time.time()

    previous_time = last_logged_events.get(
        event_name,
        0
    )

    if (
        current_time - previous_time
        >= EVENT_COOLDOWN
    ):

        last_logged_events[event_name] = (
            current_time
        )

        return True

    return False


# ============================================================
# 3. SYSTEM STARTUP
# ============================================================

print("=" * 70)

print(
    "        SIH DRONE - INTEGRATED AI DISASTER DETECTION"
)

print(
    "        SEARCH + RESCUE | HAZARD AWARENESS"
)

print(
    "        FINAL VERSION + EVENT LOGGING"
)

print("=" * 70)


# Log system startup

log_event(
    "SYSTEM START",
    details=(
        "AI disaster detection system started"
    ),
    threat_level="CLEAR"
)


# ============================================================
# 4. LOAD AI MODELS
# ============================================================

print(
    "Loading AI models..."
)


try:

    # Normal YOLO model
    #
    # Person
    # Bicycle
    # Car
    # Motorcycle
    # Bus
    # Truck

    object_model = YOLO(
        "yolo11n.pt"
    )


    # Pose model
    #
    # Used for possible fallen / lying victim detection

    pose_model = YOLO(
        "yolo11n-pose.pt"
    )


    # Fire + Smoke model
    #
    # 0 = smoke
    # 1 = fire

    fire_model = YOLO(
        "fire_smoke.pt"
    )


except Exception as error:

    print()
    print("=" * 70)

    print(
        "ERROR: AI MODEL LOADING FAILED"
    )

    print(error)

    print("=" * 70)

    raise SystemExit


print(
    "All AI models loaded successfully!"
)


# ============================================================
# 5. CAMERA
# ============================================================

print(
    "Starting camera..."
)


camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print(
        "ERROR: Camera could not be opened."
    )

    log_event(
        "CAMERA ERROR",
        details=(
            "Camera could not be opened"
        ),
        threat_level="HIGH"
    )

    raise SystemExit


print(
    "Camera opened successfully!"
)

print(
    "Press Q to stop."
)


# ============================================================
# 6. TARGET CLASSES
# ============================================================

# COCO class IDs:
#
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
# 7. SYSTEM SETTINGS
# ============================================================

OBJECT_CONFIDENCE = 0.45

FIRE_CONFIDENCE = 0.40

POSE_CONFIDENCE = 0.40


# Smaller torso angle means a more horizontal body.

VICTIM_ANGLE_THRESHOLD = 45


# ============================================================
# 8. FPS SETTINGS
# ============================================================

previous_time = time.time()

fps = 0.0


# ============================================================
# 9. TERMINAL ALERT SETTINGS
# ============================================================

last_alert_time = 0

ALERT_COOLDOWN = 3.0


# ============================================================
# 10. DASHBOARD
# ============================================================

def draw_status_panel(
    image,
    person_count,
    vehicle_count,
    fire_count,
    smoke_count,
    victim_count,
    fps_value,
    threat_level,
    events_logged,
    last_event
):

    # --------------------------------------------------------
    # Dashboard panel
    # --------------------------------------------------------

    panel_x1 = 10

    panel_y1 = 50

    panel_x2 = 360

    panel_y2 = 295


    cv2.rectangle(
        image,
        (panel_x1, panel_y1),
        (panel_x2, panel_y2),
        (20, 20, 20),
        -1
    )


    cv2.rectangle(
        image,
        (panel_x1, panel_y1),
        (panel_x2, panel_y2),
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # Dashboard title
    # --------------------------------------------------------

    cv2.putText(
        image,
        "MISSION DASHBOARD",
        (25, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # Detection counters
    # --------------------------------------------------------

    cv2.putText(
        image,
        f"PERSONS        : {person_count}",
        (25, 108),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )


    cv2.putText(
        image,
        f"VEHICLES       : {vehicle_count}",
        (25, 133),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1
    )


    cv2.putText(
        image,
        f"FIRE           : {fire_count}",
        (25, 158),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (0, 0, 255),
        2
    )


    cv2.putText(
        image,
        f"SMOKE          : {smoke_count}",
        (25, 183),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (0, 165, 255),
        2
    )


    cv2.putText(
        image,
        f"POSSIBLE VICT. : {victim_count}",
        (25, 208),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (0, 255, 0),
        2
    )


    cv2.putText(
        image,
        f"FPS            : {fps_value:.1f}",
        (25, 233),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (255, 255, 255),
        1
    )


    cv2.putText(
        image,
        f"EVENTS LOGGED  : {events_logged}",
        (25, 258),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (255, 255, 255),
        1
    )


    # --------------------------------------------------------
    # Threat indicator
    # --------------------------------------------------------

    if threat_level == "HIGH":

        threat_color = (0, 0, 255)

    elif threat_level == "MEDIUM":

        threat_color = (0, 165, 255)

    else:

        threat_color = (0, 255, 0)


    h, w = image.shape[:2]


    threat_x1 = max(
        w - 300,
        375
    )

    threat_y1 = 50

    threat_x2 = w - 10

    threat_y2 = 95


    cv2.rectangle(
        image,
        (threat_x1, threat_y1),
        (threat_x2, threat_y2),
        (20, 20, 20),
        -1
    )


    cv2.rectangle(
        image,
        (threat_x1, threat_y1),
        (threat_x2, threat_y2),
        threat_color,
        2
    )


    cv2.putText(
        image,
        f"THREAT: {threat_level}",
        (
            threat_x1 + 12,
            threat_y1 + 30
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        threat_color,
        2
    )


    # --------------------------------------------------------
    # Last event
    # --------------------------------------------------------

    short_event = last_event

    if len(short_event) > 28:

        short_event = (
            short_event[:28]
        )


    cv2.rectangle(
        image,
        (threat_x1, 108),
        (w - 10, 148),
        (20, 20, 20),
        -1
    )


    cv2.putText(
        image,
        f"LAST EVENT: {short_event}",
        (
            threat_x1 + 8,
            134
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1
    )


# ============================================================
# 11. THREAT ASSESSMENT
# ============================================================

def calculate_threat_level(
    fire_count,
    smoke_count,
    victim_count
):

    if fire_count > 0:

        return "HIGH"


    if (
        victim_count > 0
        and smoke_count > 0
    ):

        return "HIGH"


    if (
        smoke_count > 0
        or victim_count > 0
    ):

        return "MEDIUM"


    return "CLEAR"


# ============================================================
# 12. TERMINAL ALERT
# ============================================================

def print_event_alert(
    fire_count,
    smoke_count,
    victim_count,
    threat_level
):

    global last_alert_time


    current_time = time.time()


    if (
        current_time - last_alert_time
        < ALERT_COOLDOWN
    ):

        return


    alert_message = None


    if fire_count > 0:

        alert_message = (
            "FIRE DETECTED - IMMEDIATE HAZARD"
        )


    elif (
        victim_count > 0
        and smoke_count > 0
    ):

        alert_message = (
            "POSSIBLE VICTIM + SMOKE DETECTED"
        )


    elif victim_count > 0:

        alert_message = (
            "POSSIBLE VICTIM DETECTED"
        )


    elif smoke_count > 0:

        alert_message = (
            "SMOKE DETECTED - CHECK AREA"
        )


    if alert_message is not None:

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )


        print()

        print(
            "!" * 60
        )

        print(
            f"[{timestamp}] ALERT: "
            f"{alert_message}"
        )

        print(
            f"THREAT LEVEL: "
            f"{threat_level}"
        )

        print(
            "!" * 60
        )

        print()


        last_alert_time = current_time


# ============================================================
# 13. MAIN LOOP
# ============================================================

try:

    while True:

        # ----------------------------------------------------
        # Camera frame
        # ----------------------------------------------------

        ret, frame = camera.read()


        if not ret:

            print(
                "ERROR: Could not read camera frame."
            )

            log_event(
                "CAMERA ERROR",
                details=(
                    "Could not read camera frame"
                ),
                threat_level="HIGH"
            )

            break


        # ----------------------------------------------------
        # FPS
        # ----------------------------------------------------

        current_time = time.time()


        time_difference = (
            current_time
            - previous_time
        )


        if time_difference > 0:

            fps = (
                1.0
                / time_difference
            )


        previous_time = current_time


        # ----------------------------------------------------
        # Reset counters
        # ----------------------------------------------------

        person_count = 0

        vehicle_count = 0

        fire_count = 0

        smoke_count = 0

        victim_count = 0


        display = frame.copy()


        # ====================================================
        # 14. PERSON + VEHICLE DETECTION
        # ====================================================

        object_results = object_model(
            frame,
            conf=OBJECT_CONFIDENCE,
            classes=list(
                TARGET_CLASSES.keys()
            ),
            verbose=False
        )


        highest_person_confidence = 0.0


        for result in object_results:

            if result.boxes is None:

                continue


            for box in result.boxes:

                confidence = float(
                    box.conf[0]
                )


                class_id = int(
                    box.cls[0]
                )


                if (
                    class_id
                    not in TARGET_CLASSES
                ):

                    continue


                label = TARGET_CLASSES[
                    class_id
                ]


                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                # ------------------------------------------------
                # Person
                # ------------------------------------------------

                if class_id == 0:

                    person_count += 1


                    if (
                        confidence
                        > highest_person_confidence
                    ):

                        highest_person_confidence = (
                            confidence
                        )


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
                        (
                            x1,
                            max(y1 - 10, 20)
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 0, 0),
                        2
                    )


                # ------------------------------------------------
                # Vehicle / obstacle
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
                        (
                            x1,
                            max(y1 - 10, 20)
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2
                    )


        # ----------------------------------------------------
        # Log person detection
        # ----------------------------------------------------

        if person_count > 0:

            if should_log_event(
                "PERSON DETECTED"
            ):

                log_event(
                    "PERSON DETECTED",
                    f"{highest_person_confidence:.2f}",
                    person_count,
                    (
                        "Person detected by "
                        "AI object detection"
                    ),
                    "CLEAR"
                )


        # ====================================================
        # 15. FIRE + SMOKE DETECTION
        # ====================================================

        fire_results = fire_model(
            frame,
            conf=FIRE_CONFIDENCE,
            verbose=False
        )


        highest_fire_confidence = 0.0

        highest_smoke_confidence = 0.0


        for result in fire_results:

            if result.boxes is None:

                continue


            for box in result.boxes:

                confidence = float(
                    box.conf[0]
                )


                class_id = int(
                    box.cls[0]
                )


                # Fire/smoke model:
                #
                # 0 = smoke
                # 1 = fire

                if class_id == 0:

                    label = "SMOKE"

                    smoke_count += 1


                    if (
                        confidence
                        > highest_smoke_confidence
                    ):

                        highest_smoke_confidence = (
                            confidence
                        )


                elif class_id == 1:

                    label = "FIRE"

                    fire_count += 1


                    if (
                        confidence
                        > highest_fire_confidence
                    ):

                        highest_fire_confidence = (
                            confidence
                        )


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
                    (
                        x1,
                        max(y1 - 10, 20)
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 0, 255),
                    2
                )


        # ----------------------------------------------------
        # Log fire
        # ----------------------------------------------------

        if fire_count > 0:

            if should_log_event(
                "FIRE DETECTED"
            ):

                log_event(
                    "FIRE DETECTED",
                    f"{highest_fire_confidence:.2f}",
                    fire_count,
                    (
                        "Fire detected by "
                        "AI fire/smoke model"
                    ),
                    "HIGH"
                )


        # ----------------------------------------------------
        # Log smoke
        # ----------------------------------------------------

        if smoke_count > 0:

            if should_log_event(
                "SMOKE DETECTED"
            ):

                log_event(
                    "SMOKE DETECTED",
                    f"{highest_smoke_confidence:.2f}",
                    smoke_count,
                    (
                        "Smoke detected by "
                        "AI fire/smoke model"
                    ),
                    "MEDIUM"
                )


        # ====================================================
        # 16. VICTIM / POSE DETECTION
        # ====================================================

        pose_results = pose_model(
            frame,
            conf=POSE_CONFIDENCE,
            verbose=False
        )


        smallest_victim_angle = None


        for result in pose_results:

            if result.keypoints is None:

                continue


            if result.keypoints.xy is None:

                continue


            keypoints = (
                result.keypoints.xy
            )


            if len(keypoints) == 0:

                continue


            # Process every detected person.

            for person_index in range(
                len(keypoints)
            ):

                points = (
                    keypoints[
                        person_index
                    ]
                )


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


                # ------------------------------------------------
                # Validate coordinates
                # ------------------------------------------------

                if (
                    float(left_shoulder[0]) == 0
                    or float(right_shoulder[0]) == 0
                    or float(left_hip[0]) == 0
                    or float(right_hip[0]) == 0
                ):

                    continue


                # ------------------------------------------------
                # Shoulder centre
                # ------------------------------------------------

                shoulder_x = (
                    float(left_shoulder[0])
                    + float(right_shoulder[0])
                ) / 2


                shoulder_y = (
                    float(left_shoulder[1])
                    + float(right_shoulder[1])
                ) / 2


                # ------------------------------------------------
                # Hip centre
                # ------------------------------------------------

                hip_x = (
                    float(left_hip[0])
                    + float(right_hip[0])
                ) / 2


                hip_y = (
                    float(left_hip[1])
                    + float(right_hip[1])
                ) / 2


                # ------------------------------------------------
                # Body direction
                # ------------------------------------------------

                dx = (
                    hip_x
                    - shoulder_x
                )


                dy = (
                    hip_y
                    - shoulder_y
                )


                angle = abs(
                    math.degrees(
                        math.atan2(
                            dy,
                            dx
                        )
                    )
                )


                # Normalize angle

                if angle > 90:

                    angle = (
                        180 - angle
                    )


                # =================================================
                # POSSIBLE VICTIM
                # =================================================

                if (
                    angle
                    < VICTIM_ANGLE_THRESHOLD
                ):

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


                    if (
                        len(xs) > 0
                        and len(ys) > 0
                    ):

                        victim_count += 1


                        if (
                            smallest_victim_angle
                            is None
                            or angle
                            < smallest_victim_angle
                        ):

                            smallest_victim_angle = (
                                angle
                            )


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
                            (
                                "POSSIBLE VICTIM "
                                f"{angle:.0f}deg"
                            ),
                            (
                                x1,
                                max(y1 - 10, 20)
                            ),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65,
                            (0, 255, 0),
                            2
                        )


        # ----------------------------------------------------
        # Log possible victim
        # ----------------------------------------------------

        if victim_count > 0:

            if should_log_event(
                "POSSIBLE VICTIM"
            ):

                angle_text = ""


                if (
                    smallest_victim_angle
                    is not None
                ):

                    angle_text = (
                        "Torso angle "
                        f"{smallest_victim_angle:.1f} degrees"
                    )


                log_event(
                    "POSSIBLE VICTIM",
                    "",
                    victim_count,
                    (
                        "Possible fallen/lying "
                        "victim detected using "
                        "pose analysis. "
                        + angle_text
                    ),
                    "HIGH"
                )


        # ====================================================
        # 17. THREAT ASSESSMENT
        # ====================================================

        threat_level = (
            calculate_threat_level(
                fire_count,
                smoke_count,
                victim_count
            )
        )


        # ----------------------------------------------------
        # Threat logging
        # ----------------------------------------------------

        if threat_level == "HIGH":

            if should_log_event(
                "THREAT LEVEL HIGH"
            ):

                log_event(
                    "THREAT LEVEL HIGH",
                    details=(
                        "High-risk condition "
                        "detected"
                    ),
                    threat_level="HIGH"
                )


        elif threat_level == "MEDIUM":

            if should_log_event(
                "THREAT LEVEL MEDIUM"
            ):

                log_event(
                    "THREAT LEVEL MEDIUM",
                    details=(
                        "Potential hazard "
                        "condition detected"
                    ),
                    threat_level="MEDIUM"
                )


        # ----------------------------------------------------
        # Terminal alert
        # ----------------------------------------------------

        print_event_alert(
            fire_count,
            smoke_count,
            victim_count,
            threat_level
        )


        # ====================================================
        # 18. SYSTEM TITLE
        # ====================================================

        cv2.putText(
            display,
            "SIH DRONE - AI DISASTER DETECTION",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        # ====================================================
        # 19. DASHBOARD
        # ====================================================

        draw_status_panel(
            display,
            person_count,
            vehicle_count,
            fire_count,
            smoke_count,
            victim_count,
            fps,
            threat_level,
            total_events_logged,
            last_event_text
        )


        # ====================================================
        # 20. STATUS MESSAGE
        # ====================================================

        if threat_level == "HIGH":

            status_message = (
                "!!! EMERGENCY - "
                "RESPONDER CAUTION !!!"
            )


        elif threat_level == "MEDIUM":

            status_message = (
                "CAUTION - POTENTIAL HAZARD"
            )


        else:

            status_message = (
                "AREA STATUS: CLEAR"
            )


        cv2.putText(
            display,
            status_message,
            (
                20,
                display.shape[0] - 20
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        # ====================================================
        # 21. CURRENT TIME
        # ====================================================

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )


        cv2.putText(
            display,
            timestamp,
            (
                display.shape[1] - 100,
                30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )


        # ====================================================
        # 22. DISPLAY
        # ====================================================

        cv2.imshow(
            "SIH Drone - Integrated Detection",
            display
        )


        # ====================================================
        # 23. QUIT
        # ====================================================

        if (
            cv2.waitKey(1) & 0xFF
            == ord("q")
        ):

            break


# ============================================================
# 24. ERROR HANDLING
# ============================================================

except KeyboardInterrupt:

    print()

    print(
        "System interrupted by user."
    )


except Exception as error:

    print()

    print("=" * 60)

    print(
        "RUNTIME ERROR:"
    )

    print(error)

    print("=" * 60)


    log_event(
        "SYSTEM ERROR",
        details=str(error),
        threat_level="HIGH"
    )


# ============================================================
# 25. CLEANUP
# ============================================================

finally:

    camera.release()

    cv2.destroyAllWindows()


    log_event(
        "SYSTEM STOP",
        details=(
            "AI disaster detection "
            "system stopped"
        ),
        threat_level="CLEAR"
    )


    print()

    print("=" * 60)

    print(
        "Integrated detection stopped."
    )

    print(
        "SIH Drone system shutdown complete."
    )

    print(
        f"Total events logged: "
        f"{total_events_logged}"
    )

    print(
        f"Event log file: "
        f"{LOG_FILE}"
    )

    print("=" * 60)