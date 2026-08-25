# SIH Drone - AI Based Disaster Detection and Rescue Support System

## About the Project

This project is developed as part of the Smart India Hackathon.

Our idea is to use a group of drones to support search and rescue operations during disasters. When a disaster occurs, the drones can be deployed to the affected area and work together to find people, identify hazards and help maintain communication.

The main aim is to reduce the time taken to locate victims and also reduce the risk faced by rescue teams while entering dangerous areas.

## What Our Drone System Does

The system is designed around multiple drones working together.

Each drone can be used for different tasks depending on the situation. The drones can move around the disaster area, collect information and send it back to the rescue team.

The major functions we are working on are:

- Person detection
- Possible victim detection
- Fire detection
- Smoke detection
- Hazard detection
- Event logging
- Live detection dashboard
- Communication between drones
- Network support in areas where normal communication is unavailable

## AI Detection

For the detection part, we are using computer vision and YOLO-based models.

### Person Detection

The AI model detects people in the camera feed and displays a bounding box with the confidence value.

### Fire and Smoke Detection

A separate fire/smoke model is used to detect fire and smoke.

The detected condition is displayed on the screen and can also increase the threat level of the area.

### Victim Detection

Pose detection is used to analyse the position of a detected person.

The system checks the body posture using keypoints such as:

- Left shoulder
- Right shoulder
- Left hip
- Right hip

Based on the position of these points, the system estimates whether a person may be lying down and marks it as a possible victim.

This is only a basic detection method at the current stage and will be improved further.

## Mission Dashboard

The detection results are displayed through a simple dashboard.

The dashboard currently shows information such as:

- Number of people detected
- Number of vehicles detected
- Fire detections
- Smoke detections
- Possible victims
- FPS
- Current threat level
- Number of events logged
- Latest detected event

This gives the operator a quick overview of what is happening in the area being monitored.

## Event Logging

The system also maintains an event log in CSV format.

The log records events such as:

- System start
- System stop
- Person detected
- Smoke detected
- Fire detected
- Threat level changes

Each event contains information such as the timestamp, event type, confidence, count, details and threat level.

This can be useful for reviewing what happened during a mission.

## Drone Communication

The drones are also planned to work as communication nodes during disaster situations.

We are using ESP32 and LoRa for communication between the drones.

The idea is that when normal mobile or internet connectivity is unavailable, the drone network can help transmit basic information between the affected area and the rescue team.

The same system can also be used to pass information between multiple drones.

## Emergency Supply Support

Apart from detection and communication, the drone system can also be used to carry and deliver basic emergency supplies such as food and other necessary materials to affected people.

This can be especially useful when roads are blocked or the area is unsafe for immediate human access.

## Multiple Drone Operation

The overall concept is based on using multiple drones instead of depending on a single drone.

For example:

- One drone can search for people.
- Another drone can monitor hazards.
- Another drone can help with communication.
- Another drone can be used for emergency supply delivery.

The drones can share information and help the rescue team understand the situation before sending people into the affected area.

## Current Project Structure

```text
SIH-Drone/
│
├── main.py
├── person_detection.py
├── victim_detection.py
├── hazard_detection.py
├── fire_smoke_test.py
│
├── integrated_detection.py
├── integrated_detection_backup.py
├── integrated_detection_enhanced.py
├── integrated_detection_dashboard_fixed.py
├── integrated_detection_event_logging.py
│
├── event_log.csv
│
├── yolo_test.py
├── yolo11n.pt
├── yolo11n-pose.pt
├── fire_smoke.pt
│
└── SIH Drone Project.txt
```

Some of the files are different versions created during development and testing. They are kept in the repository to show the progress of the project.

## Technologies Used

- Python
- OpenCV
- YOLO
- ESP32
- LoRa
- Computer Vision
- Pose Detection
- CSV based event logging

## Current Status

The basic AI detection system is working.

Currently implemented and tested:

- Person detection
- Fire/smoke detection
- Basic victim detection
- Threat level indication
- Integrated camera detection
- Mission dashboard
- Event logging

The communication and multi-drone parts are being developed as part of the overall system.

## Future Improvements

The next stages of the project include:

- Better victim detection
- Improved hazard classification
- Multiple drone coordination
- LoRa based communication between drones
- Live location sharing
- Better mission control dashboard
- Emergency supply delivery mechanism
- Improved detection accuracy
- Testing in real disaster-like environments

## Project Goal

The final goal is to develop a practical drone-based system that can assist rescue teams during disasters.

Instead of sending rescue personnel directly into an unknown and potentially dangerous area, the drones can first inspect the area, identify possible victims and hazards, and provide useful information to the rescue team.

This can help rescue teams make faster and safer decisions.

## Team

Developed as a Smart India Hackathon project.
