from ultralytics import YOLO
import cv2

print("Starting SIH Drone Hazard Detection...")

# General YOLO model
model = YOLO("yolo11n.pt")

# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

print("Camera started successfully!")
print("Press Q to stop.")

# Objects that we want to monitor
HAZARD_CLASSES = {
    1: "BICYCLE",
    2: "CAR",
    3: "MOTORCYCLE",
    5: "BUS",
    7: "TRUCK"
}

CONFIDENCE_THRESHOLD = 0.50

while True:

    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break

    # Run YOLO
    results = model(
        frame,
        verbose=False,
        conf=CONFIDENCE_THRESHOLD
    )

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # Ignore objects outside our hazard list
            if class_id not in HAZARD_CLASSES:
                continue

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            hazard_name = HAZARD_CLASSES[class_id]

            label = (
                f"HAZARD: "
                f"{hazard_name} "
                f"{confidence:.2f}"
            )

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                3
            )

            # Draw label
            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 0, 255),
                2
            )

    # Title
    cv2.putText(
        frame,
        "SIH DRONE - GENERAL HAZARDS",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Display
    cv2.imshow(
        "SIH Drone - Hazard Detection",
        frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()

print("Hazard detection stopped.")