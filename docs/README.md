# BMW X5 2023 - Advanced Driver Behavior Monitor
## Complete Implementation Guide - All Phases

---

## 📋 Table of Contents

### Project Overview
1. [System Architecture](#system-architecture)
2. [Hardware Requirements](#hardware-requirements)
3. [Software Stack](#software-stack)
4. [Implementation Phases](#implementation-phases)

### Phase Documentation
- [Phase 1: OBD-II Based Monitoring](./PHASE1_README.md)
- [Phase 2: IMU + GPS Integration](./PHASE2_README.md)
- [Phase 3: AI Lane Detection](./PHASE3_README.md)

### Supporting Documentation
- [Installation Guide](./INSTALLATION_GUIDE.md)
- [Hardware Setup Guide](./HARDWARE_SETUP.md)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)
- [API Reference](./API_REFERENCE.md)

---

## System Architecture

### Modular Design Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│                  Car Behavior Monitor                       │
│                     (Main Application)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Module Manager (GUI)                   │   │
│  │  - Auto-detect available hardware                   │   │
│  │  - Enable/disable modules dynamically               │   │
│  │  - Configure module settings                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌──────────────┬──────────────┬──────────────────────┐    │
│  │   Phase 1    │   Phase 2    │      Phase 3        │    │
│  │   Module     │   Modules    │      Module         │    │
│  ├──────────────┼──────────────┼──────────────────────┤    │
│  │              │              │                      │    │
│  │ ┌──────────┐ │ ┌──────────┐ │ ┌─────────────────┐│    │
│  │ │ OBD-II   │ │ │ IMU      │ │ │ Camera          ││    │
│  │ │ Reader   │ │ │ Reader   │ │ │ + AI HAT+       ││    │
│  │ └──────────┘ │ └──────────┘ │ │ Lane Detection  ││    │
│  │              │              │ └─────────────────┘│    │
│  │              │ ┌──────────┐ │                      │    │
│  │              │ │ GPS      │ │                      │    │
│  │              │ │ Reader   │ │                      │    │
│  │              │ └──────────┘ │                      │    │
│  └──────────────┴──────────────┴──────────────────────┘    │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Data Fusion Engine                        │   │
│  │  - Timestamp synchronization                        │   │
│  │  - Cross-sensor validation                          │   │
│  │  - Metric calculation                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌──────────────────┬──────────────────────────────────┐   │
│  │   Display        │        Data Logger              │   │
│  │   Module         │        Module                   │   │
│  │   (3.5" TFT)     │        (CSV/SQLite)             │   │
│  └──────────────────┴──────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Modularity**: Each sensor/feature is an independent module
2. **Progressive Enhancement**: Each phase builds on previous phases
3. **Graceful Degradation**: System works with any subset of modules
4. **Hot-Plugging**: Modules can be enabled/disabled at runtime
5. **Hardware Auto-Detection**: System automatically detects available hardware

---

## Hardware Requirements

### Phase 1: OBD-II Only (Minimum System)

| Component | Model | Quantity | Cost | Status |
|-----------|-------|----------|------|--------|
| **Single Board Computer** | Raspberry Pi 5 4GB | 1 | $60 | Required |
| **OBD-II Adapter** | Veepeak OBDCheck BLE | 1 | $32 | ✅ Owned |
| **Display** | Waveshare 3.5" TFT | 1 | $22 | Required |
| **Power Supply** | Official Pi 5 27W USB-C | 1 | $12 | Required |
| **Storage** | MicroSD Card 32GB+ | 1 | $7 | Required |
| **Cooling** | Active Cooler | 1 | $5 | Recommended |
| | | **Total** | **~$138** | |

### Phase 2: + IMU + GPS

| Component | Addition for Phase 2 | Cost |
|-----------|---------------------|------|
| **IMU Sensor** | Adafruit BNO055 | $35 |
| **GPS Module** | NEO-7M with antenna | $13 |
| **Jumper Wires** | Female-to-Female set | $6 |
| **Mounting Hardware** | Brackets, VHB tape, etc. | $25 |
| | **Phase 2 Total** | **$79** |
| | **Cumulative** | **~$217** |

### Phase 3: + AI Lane Detection

| Component | Addition for Phase 3 | Cost |
|-----------|---------------------|------|
| **AI Accelerator** | Raspberry Pi AI HAT+ (13 TOPS) | $70 |
| **Camera** | Pi Camera Module 3 Wide | $35 |
| **Camera Cable** | CSI cable (if not included) | $5 |
| **Additional Cooling** | For AI HAT+ | $0 (included) |
| | **Phase 3 Total** | **$110** |
| | **Complete System** | **~$327** |

---

## Software Stack

### Core Framework

```
Operating System: Raspberry Pi OS (64-bit) Bookworm
Language: Python 3.11+
GUI Framework: Tkinter (built-in)
Data Storage: SQLite3 + CSV export
```

### Python Dependencies by Phase

**Phase 1:**
```bash
python-obd>=0.7.1        # OBD-II communication
pyserial>=3.5           # Serial communication
numpy>=1.24.0           # Numerical operations
pillow>=10.0.0          # Image handling for GUI
```

**Phase 2 (adds):**
```bash
adafruit-circuitpython-bno055>=1.4.0  # IMU sensor
adafruit-blinka>=8.0.0                 # Hardware abstraction
gpsd-py3>=0.3.0                        # GPS daemon interface
```

**Phase 3 (adds):**
```bash
opencv-python>=4.8.0    # Image processing
hailo-tappas           # Hailo AI runtime (Raspberry Pi OS repo)
picamera2>=0.3.0       # Camera interface
```

---

## Implementation Phases

### Phase 1: OBD-II Based Monitoring (Week 1-2)

**Objective:** Create functional driver behavior monitor using only OBD-II data

**Features:**
- ✅ Real-time vehicle speed monitoring
- ✅ Throttle position tracking
- ✅ Engine RPM monitoring
- ✅ Acceleration calculation from speed
- ✅ Harsh braking/acceleration detection
- ✅ Basic driver scoring
- ✅ Trip logging and summary
- ✅ Live dashboard display

**Deliverables:**
- Working OBD-II reader
- Real-time display application
- Data logging system
- Basic scoring algorithm
- Complete documentation

**Success Criteria:**
- System runs continuously for 30+ minutes
- All OBD-II PIDs read successfully
- Display updates smoothly (10-20 Hz)
- Data logged accurately
- Score calculation makes sense

### Phase 2: IMU + GPS Integration (Week 3-4)

**Objective:** Add direct acceleration measurement and position tracking

**Features (in addition to Phase 1):**
- ✅ 3-axis acceleration measurement (100 Hz)
- ✅ Jerk calculation
- ✅ Lateral acceleration (cornering)
- ✅ GPS position and velocity
- ✅ Velocity drift correction (OBD-II + IMU fusion)
- ✅ Enhanced scoring (includes cornering)
- ✅ Road quality detection (vibration analysis)
- ✅ Trip mapping

**Deliverables:**
- IMU integration module
- GPS integration module
- Sensor fusion algorithms
- Enhanced scoring system
- Kalman filter for velocity correction
- Updated documentation

**Success Criteria:**
- IMU reads at 100 Hz reliably
- GPS acquires fix within 2 minutes
- Velocity fusion reduces drift to <2%
- Lateral acceleration captures cornering
- All sensors synchronized properly

### Phase 3: AI Lane Detection (Week 5-7)

**Objective:** Add computer vision for lane centering analysis

**Features (in addition to Phases 1 & 2):**
- ✅ Real-time lane detection (30-60 FPS)
- ✅ Lane centering score
- ✅ Lane departure detection
- ✅ Aggressive lane change detection
- ✅ Video recording with lane overlays
- ✅ Cross-validation (camera vs. lateral accel)
- ✅ Complete driver behavior analysis

**Deliverables:**
- AI HAT+ integration
- Camera interface
- Lane detection model (YOLOv8)
- Lane analysis algorithms
- Video recording system
- Final scoring system
- Complete system documentation

**Success Criteria:**
- Lane detection runs at 30+ FPS
- Lane centering accuracy >90%
- Video recording works reliably
- All modules work together seamlessly
- System stable for 1+ hour drives

---

## Project File Structure

```
car_monitor_project/
├── README.md                          (this file)
├── requirements_phase1.txt
├── requirements_phase2.txt
├── requirements_phase3.txt
├── setup.py
│
├── docs/
│   ├── PHASE1_README.md
│   ├── PHASE2_README.md
│   ├── PHASE3_README.md
│   ├── INSTALLATION_GUIDE.md
│   ├── HARDWARE_SETUP.md
│   ├── TROUBLESHOOTING.md
│   └── API_REFERENCE.md
│
├── common/
│   ├── __init__.py
│   ├── config.py                     # Configuration management
│   ├── logger.py                     # Data logging utilities
│   ├── display.py                    # Display base classes
│   ├── scoring.py                    # Scoring algorithms
│   └── utils.py                      # Common utilities
│
├── phase1/
│   ├── __init__.py
│   ├── obd_reader.py                 # OBD-II interface
│   ├── obd_monitor.py                # Phase 1 main application
│   ├── obd_dashboard.py              # Phase 1 GUI
│   └── README.md
│
├── phase2/
│   ├── __init__.py
│   ├── imu_reader.py                 # BNO055 interface
│   ├── gps_reader.py                 # GPS interface
│   ├── sensor_fusion.py              # Data fusion algorithms
│   ├── enhanced_monitor.py           # Phase 2 main application
│   ├── enhanced_dashboard.py         # Phase 2 GUI
│   └── README.md
│
├── phase3/
│   ├── __init__.py
│   ├── camera_reader.py              # Camera interface
│   ├── lane_detector.py              # Lane detection (AI HAT+)
│   ├── lane_analyzer.py              # Lane analysis algorithms
│   ├── complete_monitor.py           # Phase 3 main application
│   ├── complete_dashboard.py         # Phase 3 GUI
│   ├── models/
│   │   └── yolov8s_lane.hef         # Hailo model file
│   └── README.md
│
├── scripts/
│   ├── install_phase1.sh
│   ├── install_phase2.sh
│   ├── install_phase3.sh
│   ├── calibrate_imu.py
│   ├── test_obd.py
│   ├── test_imu.py
│   ├── test_gps.py
│   └── test_camera.py
│
├── data/
│   ├── logs/                         # Trip logs
│   ├── videos/                       # Recorded videos
│   └── calibration/                  # Calibration data
│
└── tests/
    ├── test_obd_reader.py
    ├── test_imu_reader.py
    ├── test_gps_reader.py
    ├── test_sensor_fusion.py
    └── test_lane_detector.py
```

---

## Getting Started

### Quick Start Guide

**1. Choose Your Starting Phase:**

```bash
# Phase 1 only (OBD-II)
cd car_monitor_project
./scripts/install_phase1.sh
python3 phase1/obd_monitor.py

# Phase 2 (OBD-II + IMU + GPS)
./scripts/install_phase2.sh
python3 phase2/enhanced_monitor.py

# Phase 3 (Complete System)
./scripts/install_phase3.sh
python3 phase3/complete_monitor.py
```

**2. Module Selection:**

The system automatically detects available hardware:
- OBD-II adapter (Bluetooth)
- IMU sensor (I2C)
- GPS module (UART)
- Camera + AI HAT+

You can manually enable/disable modules in the GUI.

**3. First Run:**

```bash
# Test OBD-II connection
python3 scripts/test_obd.py

# Run Phase 1 application
python3 phase1/obd_monitor.py
```

---

## Key Features by Phase

### Phase 1 Features

| Feature | Description |
|---------|-------------|
| **Real-time Display** | Live dashboard showing speed, RPM, throttle |
| **Acceleration Calc** | Derived from speed changes |
| **Event Detection** | Harsh braking, aggressive acceleration |
| **Trip Logging** | CSV export of all data |
| **Basic Scoring** | Simple driver behavior score (0-100) |
| **Trip Summary** | Statistics at end of trip |

### Phase 2 Adds

| Feature | Description |
|---------|-------------|
| **Direct Acceleration** | 3-axis IMU @ 100 Hz (much more accurate) |
| **Lateral Forces** | Cornering/lane change detection |
| **Jerk Measurement** | Smoothness of driving |
| **GPS Tracking** | Position logging, route mapping |
| **Velocity Fusion** | Corrects IMU drift with OBD-II speed |
| **Enhanced Scoring** | Includes cornering, jerk, road quality |

### Phase 3 Adds

| Feature | Description |
|---------|-------------|
| **Lane Detection** | Real-time @ 30-60 FPS |
| **Lane Centering** | Score how well driver stays centered |
| **Lane Departure** | Alert when drifting |
| **Aggressive Changes** | Detect unsafe lane changes |
| **Video Recording** | With lane overlays |
| **Complete Scoring** | All aspects of driving behavior |

---

## Performance Targets

### Phase 1
- OBD-II update rate: 10-20 Hz ✅
- Display refresh: 10 Hz ✅
- CPU usage: <30% ✅
- Memory usage: <300 MB ✅

### Phase 2
- IMU sample rate: 100 Hz ✅
- GPS update rate: 1-10 Hz ✅
- Sensor fusion: Real-time ✅
- CPU usage: <40% ✅
- Memory usage: <500 MB ✅

### Phase 3
- Lane detection: 30-60 FPS ✅
- Camera resolution: 640×640 ✅
- Total CPU usage: <50% ✅
- AI HAT+ utilization: <80% ✅
- Memory usage: <700 MB ✅

---

## Data Storage

### Log File Formats

**Phase 1: OBD-II Only**
```csv
timestamp,speed_kph,throttle_pct,rpm,accel_calculated,event_type,score
2025-01-15 10:30:01.123,45.2,35,2100,1.2,normal,85
2025-01-15 10:30:01.223,46.1,38,2150,0.9,normal,85
...
```

**Phase 2: + IMU + GPS**
```csv
timestamp,speed_kph,throttle_pct,rpm,accel_x,accel_y,accel_z,jerk,lat,lon,gps_speed,score
2025-01-15 10:30:01.123,45.2,35,2100,1.2,0.3,-9.8,2.1,39.2904,-76.6122,45.8,87
...
```

**Phase 3: + Lane Detection**
```csv
timestamp,speed_kph,...,lane_center_offset,lane_confidence,lane_event,video_frame
2025-01-15 10:30:01.123,45.2,...,0.15,0.92,centered,frame_12345.jpg
...
```

### Database Schema

SQLite database for trip summaries:
```sql
CREATE TABLE trips (
    id INTEGER PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    distance_km REAL,
    duration_sec INTEGER,
    avg_speed REAL,
    max_speed REAL,
    harsh_braking_count INTEGER,
    aggressive_accel_count INTEGER,
    avg_score REAL,
    phase INTEGER  -- 1, 2, or 3
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER,
    timestamp TIMESTAMP,
    event_type TEXT,
    severity TEXT,
    speed_kph REAL,
    details TEXT,
    FOREIGN KEY (trip_id) REFERENCES trips(id)
);
```

---

## Safety & Legal Considerations

### Important Warnings

⚠️ **DO NOT:**
- Use this system as a substitute for attentive driving
- Rely on it for safety-critical decisions
- Interact with the display while driving
- Block airbag deployment zones with hardware

✅ **DO:**
- Review data after trips, not during
- Mount hardware securely
- Ensure nothing obstructs view
- Comply with local laws regarding dashcams
- Get passenger to interact with system while driving

### Privacy Considerations

- GPS data includes location tracking
- Video recordings may capture other vehicles/people
- Consider privacy laws in your region
- Don't share recordings without consent
- Implement data retention policies

---

## Support & Community

### Getting Help

**Documentation:**
- Phase-specific README files
- Installation guides
- Troubleshooting guide
- API reference

**Common Issues:**
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Check sensor connections
- Verify software versions
- Review log files

**Reporting Issues:**
- Include phase number
- Describe hardware configuration
- Provide log excerpts
- List steps to reproduce

---

## License & Credits

**Project License:** MIT License

**Third-Party Libraries:**
- python-obd: GPLv2
- Adafruit CircuitPython: MIT
- OpenCV: Apache 2.0
- Hailo Runtime: Hailo EULA

**Hardware Acknowledgments:**
- Raspberry Pi Foundation
- Adafruit Industries
- Hailo Technologies

---

## Version History

**v1.0.0** - Initial Release
- Phase 1: OBD-II monitoring complete
- Phase 2: IMU + GPS integration complete
- Phase 3: AI lane detection complete
- Full documentation
- Installation scripts
- Test suite

---

## Next Steps

1. **Read** the appropriate phase documentation:
   - [Phase 1 README](./PHASE1_README.md) - Start here
   - [Phase 2 README](./PHASE2_README.md)
   - [Phase 3 README](./PHASE3_README.md)

2. **Install** hardware per [Hardware Setup Guide](./HARDWARE_SETUP.md)

3. **Run** installation script for your target phase

4. **Test** each component individually

5. **Launch** the integrated application

6. **Drive** and collect data!

7. **Analyze** your driving behavior

8. **Improve** your driving based on insights

---

**Ready to get started? Head to [PHASE1_README.md](./PHASE1_README.md)!**
