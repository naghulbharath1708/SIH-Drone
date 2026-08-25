from ultralytics import YOLO
import cv2

print("Starting SIH Drone Person Detection...")

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open laptop camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

print("Camera started successfully!")
print("Press Q to stop.")

while True:

    # Read camera frame
    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break

    # Run YOLO detection
    results = model(frame, verbose=False)

    # Process detected objects
    for result in results:

        for box in result.boxes:

            # Get class ID
            class_id = int(box.cls[0])

            # Get confidence
            confidence = float(box.conf[0])
            if confidence < 0.5:
                continue
            
            # YOLO class 0 = person
            if class_id == 0:

                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 255, 255),
                    2
                )

                # Create label
                label = f"PERSON {confidence:.2f}"

                # Display label
                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

    # Show camera
    cv2.imshow("SIH Drone - Person Detection", frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Close everything
camera.release()
cv2.destroyAllWindows()

print("Person detection stopped.")