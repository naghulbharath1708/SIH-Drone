# 🚁 SIH Drone — AI-Powered Disaster Response & Emergency Communication System

> **Smart India Hackathon (SIH) Project**  
> **An autonomous multi-drone disaster-response concept combining AI-based victim/hazard detection, emergency communication, and essential-supply delivery.**

---

## 🌍 Project Overview

**SIH Drone** is a deployable multi-drone disaster-response system designed to support people and rescue teams during situations such as floods, earthquakes, landslides, cyclones, building collapses, and other communication-disrupting disasters.

When a disaster occurs, a fleet of drones can be deployed into the affected area.

The drones are designed to perform multiple coordinated roles:

- 🧍 Detect victims and people using AI
- ⚠️ Identify potential hazards such as fire and smoke
- 📡 Establish emergency communication where normal network infrastructure is unavailable
- 📦 Deliver essential food and emergency supplies
- 🛰️ Relay information between drones and the rescue/control station
- 🗺️ Provide a live/schematic operational view of the disaster area
- 📝 Maintain event and detection logs for mission monitoring

The overall goal is to **reduce victim discovery time, improve responder safety, maintain communication, and provide immediate assistance before conventional rescue infrastructure is fully restored.**

---

# 🎯 Problem Statement

> **"A deployable AI-powered autonomous drone that aids search-and-rescue operations by detecting people and hazards, thereby improving responder safety and reducing victim discovery time."**

### The disaster-response challenge

After a major disaster:

- Communication towers may become unavailable.
- Roads may be blocked.
- Rescue teams may not immediately know where victims are located.
- Entering dangerous areas can expose responders to additional risks.
- Victims may require food, water, and basic emergency supplies before rescue teams reach them.

A conventional response can therefore be delayed by **poor visibility, inaccessible terrain, and communication loss**.

---

# 💡 Our Proposed Solution

We propose a **multi-drone disaster-response network** in which drones are deployed as a coordinated fleet.

Each drone can perform one or more mission roles depending on the situation.

```text
                         ┌─────────────────────┐
                         │   RESCUE COMMAND    │
                         │     / CONTROL       │
                         └──────────┬──────────┘
                                    │
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
                 ┌───────────┐             ┌───────────┐
                 │ Drone D1  │◄───────────►│ Drone D2  │
                 │ AI Search │    LoRa     │ AI Search │
                 └─────┬─────┘             └─────┬─────┘
                       │                         │
                       │                         │
                       ▼                         ▼
                 ┌───────────┐             ┌───────────┐
                 │ Drone D3  │◄───────────►│ Drone D4  │
                 │ AI Search │    LoRa     │ Supply /  │
                 │ / Relay   │             │ Support   │
                 └───────────┘             └───────────┘
```

The fleet can create a communication and information network over the affected region while simultaneously searching for victims and hazards.

---

# 🚨 Disaster Mission Workflow

## Step 1 — Disaster Occurs

A disaster affects an area and may damage:

- Mobile towers
- Internet infrastructure
- Roads
- Power infrastructure
- Conventional communication systems

---

## Step 2 — Drone Fleet Deployment

A set of drones is deployed into the affected area.

For example:

```text
D1 → Search / Detection
D2 → Search / Detection
D3 → Search / Communication Relay
D4 → Supply / Search Support
```

The exact role allocation can change according to mission requirements.

---

## Step 3 — AI-Based Area Scanning

The drones/camera system scans the disaster area.

The AI pipeline can detect:

- 👤 People
- 🚗 Vehicles / objects
- 🔥 Fire
- 💨 Smoke
- 🧍 Possible victims using pose estimation

Detected objects are highlighted with bounding boxes and confidence values.

---

## Step 4 — Victim Detection

The pose-estimation system analyses human body keypoints.

The current prototype uses important keypoints such as:

```text
Left Shoulder
Right Shoulder
Left Hip
Right Hip
```

The relative position of these points is used to estimate body orientation.

A sufficiently horizontal body posture can be flagged as:

```text
POSSIBLE VICTIM
```

> This is an AI-assisted indication, not a medical diagnosis or definitive confirmation of a victim's condition.

---

## Step 5 — Hazard Detection

The AI system can identify:

```text
FIRE
SMOKE
```

Hazard detections contribute to the operational threat assessment.

Example:

```text
THREAT: CLEAR
```

or:

```text
THREAT: MEDIUM
```

This allows the rescue team to prioritize potentially dangerous areas.

---

# 📡 Emergency Communication Network

One of the major concepts of the project is maintaining communication when normal cellular/internet infrastructure is unavailable.

## LoRa + ESP32

The proposed communication layer uses:

- **ESP32**
- **LoRa communication**
- Drone-to-drone communication
- Drone-to-ground/control communication

LoRa is intended to provide **long-range, low-power emergency data communication** between nodes.

The drones can act as distributed communication nodes/relays so that information can continue to move across the disaster area even when conventional communication infrastructure is unavailable.

### Important distinction

LoRa itself does **not** directly provide normal internet access.

Instead, the system can provide an **emergency communication/data network**. A suitable gateway can bridge that network to the internet whenever an internet connection is available.

This architecture can therefore support communication in areas where cellular coverage is damaged or unavailable.

---

# 📦 Emergency Food & Supply Delivery

The drone fleet can also support immediate humanitarian requirements.

A designated drone can carry lightweight emergency supplies such as:

- Food packets
- Water
- Basic first-aid supplies
- Emergency communication equipment
- Other lightweight essential materials

The concept is to deliver immediate assistance to identified locations while rescue teams are still travelling to the area.

> Payload capacity, delivery mechanism, flight time, and safety limits must be validated during the hardware-development stage.

---

# 🗺️ Disaster Area Live Map

The project includes a mission-map concept for monitoring drone positions and detected locations.

A typical operational view can show:

```text
              DISASTER AREA — LIVE MAP

        D4
         \
          \       D3
           \     /
            \   /
             D2
              \
               D1 -------- RC
```

The map can represent:

- Drone locations
- Approximate communication coverage
- Victim detection
- Mission routes
- Rescue command location
- Communication links
- Areas requiring attention

The current map representation is **schematic and not intended to be geographically accurate**.

---

# 📊 Mission Dashboard

The AI detection system provides a real-time mission dashboard.

Example information:

```text
MISSION DASHBOARD

PERSONS       : 1
VEHICLES      : 0
FIRE          : 0
SMOKE         : 1
POSSIBLE VICT.: 0
FPS           : 5.9
EVENTS LOGGED : 5

THREAT: MEDIUM
AREA STATUS: ATTENTION REQUIRED
```

The dashboard provides the operator with a quick summary of the current AI-detected situation.

---

# 📝 Event Logging

Important system events are stored in:

```text
event_log.csv
```

The log records:

| Field | Description |
|---|---|
| Timestamp | Date and time |
| Event | Detection/system event |
| Confidence | AI confidence |
| Count | Number of detected objects |
| Details | Description of event |
| Threat Level | Current threat status |

Example:

```csv
Timestamp,Event,Confidence,Count,Details,Threat Level
2026-08-25 12:44:55,SYSTEM START,,,AI disaster detection system started,CLEAR
2026-08-25 12:44:58,PERSON DETECTED,0.88,1,Person detected by AI object detection,CLEAR
2026-08-25 12:45:03,SMOKE DETECTED,0.61,1,Smoke detected by AI fire/smoke model,MEDIUM
2026-08-25 12:45:05,THREAT LEVEL MEDIUM,,,Potential hazard condition detected,MEDIUM
```

This creates a persistent mission history that can be reviewed after a test or operation.

---

# 🧠 AI Detection Architecture

The current computer-vision prototype combines multiple AI components.

```text
                   CAMERA / VIDEO INPUT
                           │
                           ▼
                 ┌─────────────────────┐
                 │   OpenCV Pipeline   │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │ YOLO Object  │  │ Fire/Smoke   │  │ YOLO Pose    │
   │ Detection    │  │ Detection    │  │ Estimation   │
   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Detection Analysis  │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Threat Assessment   │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Dashboard       Event Log      Alerts/
        Display         CSV History    Decisions
```

---

# 🤖 AI Models

The repository currently contains:

```text
yolo11n.pt
yolo11n-pose.pt
fire_smoke.pt
```

| Model | Role |
|---|---|
| `yolo11n.pt` | Object/person detection |
| `yolo11n-pose.pt` | Human pose/keypoint estimation |
| `fire_smoke.pt` | Fire and smoke detection |

---

# 🔌 Hardware Concept

The future integrated hardware architecture is based around:

```text
                    ┌───────────────┐
                    │     ESP32     │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │   LoRa Module  │
                    └───────┬───────┘
                            │
                    Long-range data
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
              Drone       Drone       Ground
               D1           D2         Station
```

Potential hardware modules include:

- ESP32
- LoRa transceiver
- Camera
- Drone flight controller
- GPS module
- Payload mechanism
- Battery/power system
- Sensors

Hardware selection and integration will depend on the final drone design.

---

# 🛠️ Software Technologies

- **Python**
- **OpenCV**
- **Ultralytics YOLO**
- **YOLO Object Detection**
- **YOLO Pose Estimation**
- **Computer Vision**
- **CSV Event Logging**
- **ESP32**
- **LoRa Communication**
- **Git**
- **GitHub**
- **Visual Studio Code**

---

# 📁 Repository Structure

```text
SIH-Drone/
│
├── fire_smoke_test.py
├── fire_smoke.pt
├── hazard_detection.py
│
├── integrated_detection.py
├── integrated_detection_backup.py
├── integrated_detection_dashboard_fixed.py
├── integrated_detection_enhanced.py
├── integrated_detection_event_logging.py
│
├── event_log.csv
├── main.py
├── person_detection.py
├── victim_detection.py
├── yolo_test.py
│
├── yolo11n.pt
├── yolo11n-pose.pt
│
└── SIH Drone Project.txt
```

### Development Versions

The multiple integrated-detection files are intentionally retained to demonstrate development progress:

| File | Purpose |
|---|---|
| `integrated_detection.py` | Main integrated detection implementation |
| `integrated_detection_backup.py` | Backup version |
| `integrated_detection_enhanced.py` | Enhanced implementation |
| `integrated_detection_dashboard_fixed.py` | Dashboard-focused version |
| `integrated_detection_event_logging.py` | Event-logging implementation |

---

# 💻 Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SIH-Drone
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install ultralytics opencv-python
```

Additional packages required by future hardware/communication modules can be installed separately.

---

# ▶️ Running the AI Prototype

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Run the integrated detection system:

```bash
python integrated_detection.py
```

For the event-logging version:

```bash
python integrated_detection_event_logging.py
```

The system will:

1. Load the AI models.
2. Start the camera.
3. Process the video stream.
4. Detect people/objects.
5. Detect fire and smoke.
6. Analyse human pose.
7. Estimate possible-victim conditions.
8. Determine threat status.
9. Display the mission dashboard.
10. Record important events.

Press:

```text
Q
```

to stop the application.

---

# 🔄 Complete Disaster-Response Concept

The complete proposed system can be viewed as five connected layers:

```text
┌────────────────────────────────────────────────────┐
│                1. DISASTER EVENT                   │
│                                                    │
│  Flood / Earthquake / Landslide / Cyclone / etc. │
└────────────────────────┬───────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────┐
│              2. DRONE DEPLOYMENT                   │
│                                                    │
│          D1   D2   D3   D4   ...                  │
│                                                    │
│        Multi-drone search & support fleet         │
└────────────────────────┬───────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────┐
│             3. AI SEARCH & DETECTION               │
│                                                    │
│ Person │ Fire │ Smoke │ Objects │ Pose/Victim     │
└────────────────────────┬───────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────┐
│          4. COMMUNICATION & ASSISTANCE             │
│                                                    │
│ LoRa + ESP32  │  Emergency Network  │  Supplies  │
│                                                    │
│ Food / Water / Essential Payload Delivery         │
└────────────────────────┬───────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────┐
│             5. RESCUE COORDINATION                 │
│                                                    │
│ Dashboard → Event Logs → Victim Location →       │
│ Threat Information → Rescue Team                  │
└────────────────────────────────────────────────────┘
```

---

# 🎯 Operational Objectives

The system aims to:

1. **Reduce victim discovery time**
2. **Improve responder safety**
3. **Detect hazards automatically**
4. **Maintain emergency communication**
5. **Deliver essential supplies**
6. **Provide real-time operational information**
7. **Maintain mission event history**
8. **Enable coordinated multi-drone operations**

---

# 🚀 Future Development

The next stages of the project can include:

### 🛩️ Autonomous Drone Operations

- Autonomous waypoint navigation
- Automatic area coverage
- GPS-based positioning
- Return-to-home functionality
- Collision avoidance
- Multi-drone coordination

### 📡 Emergency Communication

- LoRa mesh networking
- ESP32-based communication nodes
- Drone-to-drone relaying
- Drone-to-ground communication
- Gateway-based internet backhaul when available

### 🗺️ Mission Intelligence

- GPS-tagged victim locations
- Live disaster map
- Search-area coverage tracking
- Drone health/status monitoring
- Mission route planning

### 📦 Humanitarian Support

- Automated payload delivery
- Food and water delivery
- Emergency medical supply delivery
- Payload release mechanism

### 🧠 AI Improvements

- Improved victim-condition classification
- Thermal-camera integration
- Night-time detection
- Better fire/smoke detection
- Multi-camera fusion
- Improved false-positive filtering

---

# ⚠️ Limitations & Safety

This repository contains a **student prototype and proof-of-concept**.

Important limitations include:

- AI detection performance depends on camera quality, lighting, distance, and environmental conditions.
- AI confidence does not guarantee detection correctness.
- Pose-based victim detection is currently heuristic.
- A `POSSIBLE VICTIM` result is not a medical diagnosis.
- LoRa provides low-bandwidth communication and is not itself an internet connection.
- Actual communication range depends on hardware, antenna, environment, frequency configuration, and regulations.
- Drone payload capacity, flight time, and delivery mechanisms require physical testing.
- Autonomous multi-drone operation requires additional flight-control, navigation, communication, and safety systems.
- Real-world disaster deployment requires extensive testing, regulatory compliance, and human supervision.

---

# 🏆 Expected Impact

The proposed system aims to transform a drone from a simple aerial camera into a **multi-purpose disaster-response platform**.

Instead of only observing a disaster area, the drone fleet can potentially:

```text
       SEARCH
          ↓
       DETECT
          ↓
      COMMUNICATE
          ↓
       SUPPORT
          ↓
       REPORT
          ↓
       ASSIST RESCUE
```

This combination of **AI detection + emergency communication + supply delivery + multi-drone coordination** can provide a stronger first-response capability in disaster-affected regions.

---

# 👥 Team

**Project:**  
SIH Drone — AI-Powered Disaster Response & Search-and-Rescue System

**Institution:**  
Sri Shakthi Institute of Engineering and Technology

**Competition:**  
Smart India Hackathon (SIH)

**Team:**  
SIH Drone Team

---

# 📄 License

This project is developed as a student prototype for the **Smart India Hackathon (SIH)**.

It is intended for research, demonstration, and educational purposes.

Further engineering validation, safety testing, regulatory compliance, and field trials are required before real-world deployment.
