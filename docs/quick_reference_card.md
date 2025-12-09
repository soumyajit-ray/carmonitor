# QUICK REFERENCE CARD - Car Acceleration Monitor

## Shopping List with Links

### Core Components
- [ ] **Raspberry Pi 4 (2GB)** - $45
      https://www.adafruit.com/product/4292
      
- [ ] **Adafruit BNO055 IMU** - $35
      https://www.adafruit.com/product/2472
      
- [ ] **Waveshare 3.5" TFT Display** - $22
      https://www.amazon.com/waveshare-3-5inch-RPi-LCD-Resistive-Touch/dp/B077Y6ZT7Y
      OR Adafruit PiTFT: https://www.adafruit.com/product/2441
      
- [ ] **NEO-7M GPS Module** - $13
      https://www.amazon.com/HiLetgo-GY-NEO6MV2-Controller-Ceramic-Antenna/dp/B01D1D0F5M
      
- [ ] **USB-C Power Supply (3A)** - $10
      https://www.adafruit.com/product/4298
      
- [ ] **MicroSD Card (32GB)** - $7
      https://www.amazon.com/SanDisk-Ultra-microSDXC-Memory-Adapter/dp/B073K14CVB
      
- [ ] **Female-to-Female Jumper Wires** - $6
      https://www.amazon.com/EDGELEC-Breadboard-Optional-Assorted-Multicolored/dp/B07GD2BWPY

**Total: ~$138**

---

## Pin Connections at a Glance

### BNO055 → Raspberry Pi (via Display Passthrough)
```
BNO055 Pin    Wire Color    Pi Pin#    Pi GPIO
──────────────────────────────────────────────
VIN           Red           Pin 1      3.3V
GND           Black         Pin 9      Ground
SDA           Blue/Green    Pin 3      GPIO2
SCL           Yellow        Pin 5      GPIO3
```

### GPS NEO-7M → Raspberry Pi (via Display Passthrough)
```
GPS Pin       Wire Color    Pi Pin#    Pi GPIO
──────────────────────────────────────────────
VCC           Red           Pin 4      5V
GND           Black         Pin 14     Ground
TX            Green         Pin 10     GPIO15 (RX)
RX            Yellow        Pin 8      GPIO14 (TX)
```
**Note:** GPS TX → Pi RX, GPS RX → Pi TX (crossover!)

### Display
```
Waveshare 3.5" plugs directly onto all 40 GPIO pins
Use the passthrough header on TOP for BNO055 and GPS connections
```

---

## Setup Checklist

### Hardware Assembly
- [ ] 1. Insert microSD card into Pi 4
- [ ] 2. Mount Waveshare display onto Pi 4 GPIO (all 40 pins)
- [ ] 3. Connect BNO055 to passthrough header on display
- [ ] 4. Connect GPS to passthrough header on display
- [ ] 5. Connect USB-C power
- [ ] 6. Position GPS antenna with view of sky

### Software Setup (After OS Install)
- [ ] 1. Enable I2C: `sudo raspi-config` → Interface Options → I2C → Enable
- [ ] 2. Enable UART: `sudo raspi-config` → Interface Options → Serial Port
         - Login shell over serial: **No**
         - Serial port hardware: **Yes**
- [ ] 3. Install display drivers (follow Waveshare instructions)
- [ ] 4. Install Python libraries:
```bash
sudo pip3 install adafruit-circuitpython-bno055
sudo apt-get install gpsd gpsd-clients python3-gps
```

### Testing
- [ ] 1. Test I2C: `sudo i2cdetect -y 1` (should show 0x28 or 0x29)
- [ ] 2. Test GPS: `cat /dev/serial0` (should show NMEA sentences)
- [ ] 3. Test display: boot should show on screen

---

## Critical Notes

⚠️ **BNO055 Mounting**
- MUST be rigidly mounted to car structure
- Align axes with car orientation:
  - X = Forward/backward
  - Y = Left/right
  - Z = Up/down

⚠️ **GPS First Lock**
- Needs 1-5 minutes with clear sky view
- Will be faster after first successful lock

⚠️ **Power Requirements**
- Minimum 3A USB-C supply
- Typical draw: ~900mA
- Peak draw: ~1.5A

⚠️ **Sampling Rate**
- Target: 100Hz (100 samples/second)
- Good balance of accuracy vs. processing load

---

## Troubleshooting Quick Reference

### BNO055 not detected
```bash
sudo i2cdetect -y 1
# If nothing at 0x28/0x29:
# - Check wiring
# - Verify I2C enabled
# - Check 3.3V power with multimeter
```

### GPS no data
```bash
cat /dev/serial0
# If no output:
# - Verify UART enabled
# - Check TX/RX crossover
# - Ensure GPS has sky view
# - Wait 5 minutes for first lock
```

### Display not working
- Ensure drivers installed
- Check display seated firmly on GPIO
- Verify `/boot/config.txt` settings

---

## Next Steps After Assembly

1. **Test each component individually** before integration
2. **Write data collection script** (Python)
3. **Implement display GUI** (pygame or tkinter)
4. **Add scoring algorithms**
5. **Create data logging system**
6. **Design/build enclosure**
7. **Test in vehicle**

---

## Software Architecture (Overview)

```
┌─────────────────────────────────────┐
│   Main Control Loop (100Hz)        │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐ │
│  │ BNO055      │  │ GPS Module   │ │
│  │ Reader      │  │ Reader       │ │
│  │ (I2C)       │  │ (UART)       │ │
│  └──────┬──────┘  └──────┬───────┘ │
│         │                 │         │
│  ┌──────▼─────────────────▼──────┐ │
│  │  Data Processing              │ │
│  │  - Sensor fusion              │ │
│  │  - Velocity integration       │ │
│  │  - Jerk calculation           │ │
│  │  - Scoring metrics            │ │
│  └──────┬────────────────────────┘ │
│         │                           │
│  ┌──────▼──────┐  ┌──────────────┐ │
│  │  Display    │  │ Data Logger  │ │
│  │  Update     │  │ (CSV/SQLite) │ │
│  └─────────────┘  └──────────────┘ │
└─────────────────────────────────────┘
```

---

## Key Formulas

### Velocity Integration
```
v(t) = v(t-1) + a(t) * Δt
where Δt = 0.01s (100Hz sampling)
```

### Jerk Calculation
```
j(t) = (a(t) - a(t-1)) / Δt
```

### Scoring Metrics (Examples)
```
Harsh Braking Score = count(deceleration > 5 m/s²) / total_samples
Aggressive Acceleration = count(acceleration > 3 m/s²) / total_samples
Smooth Driving Score = 1 - (mean(|jerk|) / threshold)
```

---

## Coordinate System

```
      Z (Up)
      ↑
      |
      |
      +----→ X (Forward)
     /
    /
   ↙ Y (Right)

Typical accelerations in car:
- Forward accel: 0 to 4 m/s² (normal driving)
- Braking: 0 to -8 m/s² (panic stop)
- Lateral (cornering): ±4 m/s²
- Jerk threshold: 3-5 m/s³ for "harsh"
```

---

## Resources

**Documentation:**
- Adafruit BNO055: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor
- Pi GPIO Pinout: https://pinout.xyz
- GPS NMEA: https://www.gpsinformation.org/dale/nmea.htm

**Libraries:**
- BNO055: https://github.com/adafruit/Adafruit_CircuitPython_BNO055
- GPS: https://gpsd.gitlab.io/gpsd/

**Community:**
- Raspberry Pi Forums: https://forums.raspberrypi.com
- Adafruit Forums: https://forums.adafruit.com

---

*Created for Car Acceleration Monitor Project*
*Rev 1.0 - November 2025*
