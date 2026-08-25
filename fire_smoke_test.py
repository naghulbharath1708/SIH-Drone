from ultralytics import YOLO
import cv2

model = YOLO("fire_smoke.pt")

camera = cv2.VideoCapture(0)

print("Fire-Smoke Detection Started")
print("Press Q to stop.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("ERROR: Could not read camera.")
        break

    results = model(frame, conf=0.35)

    annotated_frame = results[0].plot()

    cv2.imshow("SIH Drone - Fire & Smoke Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print("Fire-Smoke Detection Stopped.")