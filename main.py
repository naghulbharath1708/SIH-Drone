import cv2

print("Starting SIH Drone Vision System...")

# Open the laptop camera
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

    # Display live camera feed
    cv2.imshow("SIH Drone Camera", frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release camera and close window
camera.release()
cv2.destroyAllWindows()

print("Camera stopped.")