from ultralytics import YOLO
import cv2

print("Starting YOLO detection...")

# Load a pretrained YOLO model
model = YOLO("yolo11n.pt")

# Open laptop camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

print("Camera started successfully!")
print("Press Q to stop.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break

    # Run YOLO detection
    results = model(frame, verbose=False)

    # Draw detection results
    annotated_frame = results[0].plot()

    # Display the result
    cv2.imshow("SIH Drone - YOLO Detection", annotated_frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print("YOLO detection stopped.")