# Mounting Guide - Car Acceleration Monitor
## BMW X5 2023 Installation

---

## Table of Contents
1. [Critical Mounting Requirements](#critical-mounting-requirements)
2. [Recommended Mounting Locations](#recommended-mounting-locations)
3. [Mounting Strategy Overview](#mounting-strategy-overview)
4. [Detailed Mount Designs](#detailed-mount-designs)
5. [Step-by-Step Installation](#step-by-step-installation)
6. [Testing & Calibration](#testing--calibration)

---

## Critical Mounting Requirements

### For the IMU Sensor (BNO055) - MOST CRITICAL

**Requirements:**
1. ✅ **RIGID mounting** - No flex, no vibration isolation
2. ✅ **Direct connection** to vehicle body/frame
3. ✅ **Fixed orientation** - Must not rotate or shift
4. ✅ **Known axis alignment** - X/Y/Z must be aligned with car axes
5. ❌ **NO rubber/foam isolation** - Would dampen real accelerations
6. ✅ **Accessible** - For calibration and maintenance

**Why Rigid Mounting Matters:**
```
Scenario: Hard braking at -8 m/s²

Rigid mount:
  → IMU reads -8.0 m/s² (accurate)
  
Flexible mount:
  → IMU reads -6.5 m/s² initially (mount flexing absorbs force)
  → Then oscillates: -8.2, -7.8, -8.1 (spring-mass resonance)
  → INACCURATE and noisy data
```

**Axis Alignment:**
```
Car coordinate system:
       Z (Up)
       ↑
       |
       |
       +----→ X (Forward)
      /
     /
    ↙ Y (Right)

BNO055 must be mounted so its axes align:
- Sensor X-axis → Car Forward
- Sensor Y-axis → Car Right  
- Sensor Z-axis → Car Up

Or rotated 90°/180°/270° - software can correct
But must be CONSISTENT and KNOWN
```

### For the Display & Electronics (Pi + Screen)

**Requirements:**
1. ⚠️ **Vibration dampening** - Protect electronics from road shock
2. ✅ **Visible from driver & passenger** seats
3. ✅ **Doesn't obstruct view** or airbags
4. ✅ **Secure** - Won't become projectile in crash
5. ✅ **Removable** - For anti-theft
6. ⚠️ **Thermal management** - Adequate cooling airflow
7. ✅ **Cable management** - Clean, not interfering with driving

**Key Difference:**
- **IMU:** Mount rigidly TO the car
- **Display:** Mount with vibration damping NEAR the IMU

### For the GPS Antenna

**Requirements:**
1. ✅ **Clear view of sky** - Upward facing
2. ✅ **Away from metal surfaces** (reduces signal)
3. ✅ **Stable position** - Not swinging/moving
4. ⚠️ **Weather protection** if external

---

## Recommended Mounting Locations

### Primary Recommendation: Center Console

**Mount Configuration:**
```
┌─────────────────────────────────────────┐
│    Dashboard (Driver's View)            │
│                                          │
│  ┌──────────────┐                       │
│  │  Instrument  │                       │
│  │   Cluster    │                       │
│  └──────────────┘                       │
│                                          │
│         ┌─────────────┐  ← Display here │
│         │   Display   │    (angled up)  │
│         │   Unit      │                  │
│         └─────────────┘                  │
│                ↓                         │
├────────────────────────────────────────┤
│      Center Console                     │
│                                          │
│  [Cup Holders]                          │
│                                          │
│  ┌────────────────┐  ← IMU mounted here│
│  │  Storage       │    (inside console, │
│  │  Compartment   │     rigidly fixed)  │
│  └────────────────┘                     │
│                                          │
│  [Gear Shifter]                         │
│                                          │
│  [Armrest]                              │
└─────────────────────────────────────────┘
```

**Advantages:**
- ✅ IMU near vehicle center (minimal rotation effects)
- ✅ Display visible to both driver and passenger
- ✅ Close to 12V power outlet
- ✅ Close to OBD-II port (under dashboard)
- ✅ Professional appearance
- ✅ Easy to remove for security

**Disadvantages:**
- ⚠️ May require drilling or strong adhesive
- ⚠️ Limits console storage space

### Alternative: Dashboard Top Mount

**Mount Configuration:**
```
Side View:
             Windshield
               |||||
         ┌─────────────┐
         │   Display   │ ← Angled toward driver
         └──────┬──────┘
                │
    ════════════╧════════ Dashboard
    
    └─IMU mounted underneath dashboard
      (attached to metal crossbeam)
```

**Advantages:**
- ✅ Excellent visibility
- ✅ Easy installation (suction cup or adhesive pad)
- ✅ No drilling required
- ✅ Easily removable

**Disadvantages:**
- ⚠️ May obstruct view (check local laws)
- ⚠️ Less rigid IMU mounting (dashboard flex)
- ⚠️ Display exposed to sun glare
- ⚠️ Visible from outside (theft risk)

### Alternative: A-Pillar Mount

**Mount Configuration:**
```
Driver's View:

  Windshield
    |||||| 
  ╱      ╲
 ╱ ┌────┐ ╲  ← Display on A-pillar
╱  │Disp│  ╲   (driver's side)
│  └────┘   │
│           │
│  Steering │
│   Wheel   │
└───────────┘

IMU: Mounted behind pillar trim or under dashboard
```

**Advantages:**
- ✅ Good visibility for driver
- ✅ Doesn't use dashboard/console space
- ✅ Can use existing mounting points

**Disadvantages:**
- ⚠️ Only visible to driver (not passenger)
- ⚠️ May obstruct side view
- ⚠️ Difficult to make removable
- ⚠️ IMU mounting location suboptimal

---

## Mounting Strategy Overview

### Two-Part Mounting System (Recommended)

**Part 1: IMU Sensor Mount (Hidden, Permanent)**
```
Location: Inside center console or under dashboard
Method: Rigid bracket with screws/bolts
Goal: Maximum rigidity and accuracy
```

**Part 2: Display & Electronics Mount (Visible, Removable)**
```
Location: Top of center console or dashboard
Method: Quick-release bracket or strong magnets
Goal: Visibility, security, vibration protection
```

**Why Separate?**
1. IMU needs rigid mounting → permanent installation
2. Display needs visibility → exposed position
3. Electronics valuable → should be removable
4. Different vibration requirements

### Connection Strategy

**Cable Routing:**
```
Display Unit (removable)
    ↓ (short cables ~6-12")
Junction Box (semi-permanent)
    ↓ (through console/dash)
IMU Sensor (permanent, hidden)
    ↓
GPS Antenna (hidden behind dash or external)
    ↓
OBD-II Port (under dash, driver side)
```

**Using Quick-Disconnect Connectors:**
- Display unit can be removed in <10 seconds
- IMU and GPS stay installed
- No exposed wires when display removed

---

## Detailed Mount Designs

### Design 1: Professional Removable Mount (Recommended)

**Components:**

**Base Plate (Permanent):**
```
Material: 3mm aluminum plate or ABS plastic
Size: 150mm x 100mm x 3mm
Features:
- 4x mounting holes for screws to console
- Neodymium magnets embedded (4-6 pcs, N52 grade)
- Cable pass-through slot
- Non-slip rubber feet

Cost: ~$15 (DIY) or ~$30 (machined)
```

**Display Unit Housing:**
```
Material: 3D printed ABS or purchased project box
Size: 180mm x 120mm x 40mm
Features:
- Raspberry Pi 5 mounting posts
- 3.5" display window
- Ventilation slots for cooling
- Steel plate on bottom (magnetic attachment)
- Tilt adjustment mechanism (10-45° angle)

Cost: ~$10 (3D printed) or ~$20 (purchased box)
```

**IMU Bracket (Hidden, Permanent):**
```
Material: Aluminum L-bracket
Size: 50mm x 50mm x 3mm
Features:
- BNO055 mounting holes
- Rigid attachment to metal frame
- Cable strain relief
- Protective cover

Cost: ~$5
```

**Assembly:**
```
Step 1: Mount base plate to center console
        (screws + automotive adhesive)
        
Step 2: Mount IMU bracket to vehicle frame
        (inside console storage area)
        
Step 3: Route cables from IMU to base plate
        (hidden inside console)
        
Step 4: Connect display unit via magnetic attachment
        (removable for security)
```

**Advantages:**
- ✅ Professional appearance
- ✅ Strong (magnets hold ~10-20 lbs)
- ✅ Quick removal (<10 sec)
- ✅ Adjustable angle
- ✅ IMU rigidly mounted separately
- ✅ Vibration damped for electronics

### Design 2: Budget 3M VHB Tape Mount

**For Quick Prototyping:**

**Materials:**
- 3M VHB tape (double-sided, automotive grade)
- Plastic project box (for Pi + display)
- Small aluminum bracket (for IMU)
- Cable ties and adhesive wire clips

**Total Cost: ~$20-25**

**Installation:**

**IMU Mount:**
```
1. Clean mounting surface with isopropyl alcohol
2. Cut 50mm x 50mm piece of 3M VHB tape
3. Apply to aluminum L-bracket
4. Mount BNO055 to bracket with screws
5. Press firmly onto clean metal surface (dashboard frame)
6. Let cure 72 hours before use
```

**Display Mount:**
```
1. Place Pi + display in project box
2. Cut foam strips for vibration damping (3-5mm thick)
3. Apply VHB tape to foam strips
4. Attach to center console top surface
5. Box sits on foam (vibration isolated)
```

**Advantages:**
- ✅ Very cheap
- ✅ No drilling
- ✅ Removable (with effort)
- ✅ Good for testing/prototyping

**Disadvantages:**
- ⚠️ Not as secure as bolted mount
- ⚠️ VHB can fail in extreme heat
- ⚠️ Less professional appearance
- ⚠️ Difficult to reposition

### Design 3: RAM Mount System (Commercial)

**Using RAM Mounts Universal Components:**

**Parts List:**
```
- RAM X-Grip holder (for display unit): $20
- RAM double socket arm: $15
- RAM base (adhesive or drill-down): $15-25
- Custom IMU bracket: DIY

Total: ~$50-60
```

**Features:**
- ✅ Infinitely adjustable angle
- ✅ Very strong (motorcycle rated)
- ✅ Professional appearance
- ✅ Quick release
- ✅ Modular (can reposition)

**Installation:**
```
1. Mount RAM base to console/dashboard
2. Attach socket arm
3. Create custom holder for Pi+display unit
   (or use universal tablet holder)
4. Mount IMU separately (rigid bracket)
```

**Advantages:**
- ✅ Best adjustability
- ✅ Very secure
- ✅ Professional quality
- ✅ Proven in demanding environments

**Disadvantages:**
- ⚠️ More expensive
- ⚠️ Somewhat bulky
- ⚠️ Still need custom IMU solution

---

## Specific Mounting Instructions

### BMW X5 2023 Specific Mounting Points

**Recommended Location: Center Console Storage Area**

**Access:**
```
1. Open center console storage compartment
2. Remove storage tray (usually clips out)
3. Access metal crossbeam underneath
4. This is your IMU mounting location
```

**IMU Mounting:**
```
Materials needed:
- M3 or M4 screws (stainless steel)
- Washers and lock washers
- Aluminum L-bracket (50x50mm)
- Drill with bits (if no existing holes)
- Loctite (thread locker)

Steps:
1. Locate solid metal crossbeam in console
2. Mark mounting holes for bracket
3. Drill pilot holes (if needed)
4. Attach L-bracket with screws
5. Mount BNO055 to bracket
6. Verify orientation (X forward, Y right, Z up)
7. Cable routing through console to display area
```

**Display Mounting Location Options:**

**Option A: Console Top (Recommended)**
```
Location: Between cupholders and dashboard
Size constraint: ~150mm x 100mm available space
Mounting: Magnetic base or VHB tape
Visibility: Excellent for both driver and passenger
```

**Option B: Dashboard Above Climate Controls**
```
Location: Center of dash, above HVAC controls
Size constraint: ~120mm x 80mm available space
Mounting: Suction cup or adhesive pad
Visibility: Good, but may obstruct some controls
```

**Option C: Phone Mount Location**
```
Location: Dashboard vent clip or CD slot mount
Size constraint: Must fit in phone holder size
Mounting: Use phone mount adapter
Visibility: Good for driver, poor for passenger
Note: Display unit must be phone-sized (hard with Pi)
```

### GPS Antenna Placement

**Best Locations (in order):**

**1. Rear Deck/Parcel Shelf (Best)**
```
Location: Behind rear seats, under rear window
Method: Double-sided tape or velcro
Cable: Route along door seal to front
Advantages:
  ✅ Clear sky view
  ✅ Hidden from outside
  ✅ No metal obstruction
  ✅ Clean installation
```

**2. Dashboard Top (Good)**
```
Location: Top of dashboard, against windshield
Method: Double-sided tape
Cable: Route along A-pillar trim
Advantages:
  ✅ Excellent sky view
  ✅ Short cable run
Disadvantages:
  ⚠️ Visible from outside
  ⚠️ May look messy
```

**3. External (Best Signal, Most Work)**
```
Location: Roof or rear bumper
Method: Magnetic mount (if antenna has one)
Cable: Route through door/trunk seal
Advantages:
  ✅ Best possible GPS signal
  ✅ No interior metal interference
Disadvantages:
  ⚠️ Visible (potential theft)
  ⚠️ Weatherproofing needed
  ⚠️ Cable routing challenging
```

### Power Connection Points

**12V Power Options:**

**Option 1: Cigarette Lighter / 12V Socket (Easiest)**
```
Location: Center console or dashboard
Method: USB-C car adapter (5A/27W for Pi 5)
Advantages:
  ✅ No wiring needed
  ✅ Easily removable
  ✅ Can unplug when not in use
Disadvantages:
  ⚠️ Always-on (even when car off) on some vehicles
  ⚠️ May need socket for other devices
  ⚠️ Cable visible
```

**Option 2: Hardwired to Fuse Box (Best)**
```
Location: Under dashboard, driver side
Method: Add-a-fuse tap + buck converter
Advantages:
  ✅ Clean installation (no cables visible)
  ✅ Switched with ignition (auto on/off)
  ✅ Doesn't use 12V socket
Disadvantages:
  ⚠️ More complex installation
  ⚠️ Need to identify correct fuse
  ⚠️ Requires electrical knowledge
```

**Recommended Fuse Tap Setup:**
```
Materials:
- Add-a-fuse tap (appropriate for BMW fuse type)
- 12V to 5V buck converter (6A rated, adjustable)
- Fuse (5A or 10A, depending on circuit)
- USB-C cable or direct GPIO power

Connection:
12V Fuse Box (ignition-switched circuit)
    ↓
Add-a-fuse tap (with 5A or 10A fuse)
    ↓
Buck Converter (12V → 5V @ 6A)
    ↓
Raspberry Pi 5 (USB-C or GPIO pins 2,4,6)

Good fuse locations (BMW X5):
- Accessory power fuse
- Radio fuse  
- Navigation fuse
(Check owner's manual for specific numbers)
```

---

## Cable Management

### Cable Routing Strategy

**From IMU (in console) to Display (on console top):**
```
Path: Through console interior → emerge at rear of display
Length: ~30cm (12")
Protection: Wrap in split loom or spiral wrap
Attachment: Cable clips every 10cm
```

**From GPS (rear deck) to Pi:**
```
Path: Along door seal → under dash → through console
Length: ~2-3 meters
Protection: Tuck into existing trim gaps
Attachment: Adhesive clips or existing vehicle clips
```

**From OBD-II (under dash) to Pi:**
```
Path: Along center console side → into console interior
Length: ~50cm (20")
Note: Veepeak is Bluetooth, so no cable!
      Only if using USB OBD-II adapter
```

**Power Cable:**
```
From: 12V socket or fuse box
To: Display unit
Length: ~50cm - 2m (depending on source)
Protection: Use automotive-rated wire (if hardwired)
```

### Cable Organization Products

**Recommended:**
- Split loom tubing (10mm diameter): $5/3m
- Adhesive cable clips: $8/50pcs
- Spiral cable wrap: $6/5m
- Velcro cable ties: $5/50pcs
- Heat shrink tubing: $8/variety pack

**Total: ~$30**

---

## Vibration Isolation Strategy

### For the Display & Pi (Need Isolation)

**Why Isolate:**
- Protects electronics from shock
- Reduces SD card wear from vibration
- Prevents display damage
- Extends component life

**Isolation Methods:**

**Method 1: Foam Padding**
```
Material: High-density EVA foam (3-5mm thick)
Application: Between mount and electronics enclosure
Effectiveness: Good for normal driving
Cost: ~$5

Installation:
1. Cut foam to size of mounting surface
2. Adhere to bottom of enclosure
3. Mount enclosure to base plate
4. Foam compresses to 70-80% thickness (damping zone)
```

**Method 2: Rubber Grommets**
```
Material: Neoprene or silicone rubber grommets
Application: At each mounting screw point
Effectiveness: Better than foam
Cost: ~$8

Installation:
1. Drill slightly oversized holes in enclosure
2. Insert rubber grommets
3. Pass screws through grommets
4. Grommet deforms to isolate vibration
```

**Method 3: Sorbothane Pads**
```
Material: Sorbothane (viscoelastic polymer)
Application: Between mount and enclosure
Effectiveness: Excellent (used in aerospace)
Cost: ~$15-20

Installation:
1. Cut Sorbothane sheet to size (3-6mm thick)
2. Adhere to mounting surface
3. High damping coefficient (better than foam/rubber)
```

**Recommended for Your Project:**
- **Budget:** EVA foam padding (~$5)
- **Better:** Rubber grommets (~$8)
- **Best:** Sorbothane pads (~$15)

### For the IMU (NO Isolation!)

**Critical: IMU must NOT have vibration damping**

```
Wrong:
[Car Frame] → [Rubber Mount] → [IMU]
              ↑ DON'T DO THIS!
              
Correct:
[Car Frame] → [Rigid Bracket] → [IMU]
              ↑ Metal-to-metal contact
```

**Proper IMU Mounting:**
1. Metal bracket screwed directly to frame
2. IMU screwed directly to bracket
3. No rubber, foam, or springs anywhere
4. Maximum rigidity

**Exception:**
- OK to have a protective cover (not load-bearing)
- OK to have wire strain relief (doesn't affect sensor)

---

## Enclosure Design

### Display Unit Enclosure

**Option 1: Custom 3D Printed (Best)**

**Design Requirements:**
```
Dimensions: ~180mm x 120mm x 45mm (minimum)
Material: ABS or PETG (heat resistant)
Features:
- Pi 5 mounting posts (M2.5 standoffs)
- Display window cutout (3.5" screen)
- Ventilation slots (top and sides)
- Cable entry points (bottom)
- Mounting holes (for base plate attachment)
- Optional: Buttons for GPIO control
- Optional: Status LED windows

Design files: Can be created in:
- Fusion 360 (free for hobbyists)
- FreeCAD (open source)
- Tinkercad (simple, web-based)

Printing cost: ~$10-15 if you have printer
              ~$30-50 if ordering from service
```

**STL Files:** I can provide a basic design if needed

**Option 2: Modify Existing Project Box**

**Hammond 1591XXLBK or similar:**
```
Size: 190mm x 110mm x 60mm
Material: ABS plastic
Cost: ~$15-20
Modifications needed:
- Cut window for display
- Drill mounting holes for Pi
- Drill ventilation holes
- Cut cable entry slots
```

**Tools needed:**
- Dremel or rotary tool
- Step drill bits
- File for smoothing edges
- Drill

**Option 3: Commercial Raspberry Pi Case (Compromise)**

**Official Pi 5 Case + Modifications:**
```
Base: Official Pi 5 case (~$10)
Modifications:
- Remove lid
- Mount display on top
- Add custom bracket for mounting
- Add extension for extra height

Result: Quick but less professional
```

### IMU Protective Housing

**Simple Weather-Resistant Cover:**

```
Design:
┌─────────────────┐
│   ┌─────────┐   │  ← Plastic cover (not touching sensor)
│   │ BNO055  │   │
│   └────┬────┘   │
│        │        │
├────────┴────────┤
│  Metal Bracket  │  ← Rigid mounting bracket
└─────────────────┘
         │
    [Car Frame]     ← Bolted connection

Material: 3D printed or small plastic box
Purpose: Protect from dust/moisture, not impacts
Important: Cover must not contact sensor mounting
```

---

## Testing & Calibration

### Initial Installation Tests

**Test 1: Mounting Rigidity**
```
Method:
1. Mount everything
2. Apply firm hand pressure to IMU bracket
3. Sensor should not move AT ALL
4. If it flexes even slightly → add reinforcement

Pass criteria: Zero detectable movement
```

**Test 2: Axis Alignment Verification**
```
Method:
1. Park on level ground
2. Read IMU acceleration
3. Should read: X=0, Y=0, Z=9.8 m/s² (gravity)
4. If not, check orientation and mounting

Software check:
import board
import adafruit_bno055

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

print(f"Accel: {sensor.acceleration}")
# Expected: (0, 0, 9.8) when stationary
```

**Test 3: Display Visibility**
```
Method:
1. Sit in driver's seat (normal position)
2. Check display is readable without leaning
3. Sit in passenger seat
4. Check display is readable
5. Adjust angle if needed

Pass criteria: Both occupants can read easily
```

**Test 4: Vibration Check**
```
Method:
1. Start engine (idle)
2. Check display for excessive shaking
3. If visible shaking → add more damping
4. Check IMU readings for excessive noise
5. If IMU noisy → check mount rigidity

Pass criteria: Display stable, IMU clean signal
```

### Calibration Procedure

**BNO055 Calibration (Required):**

The BNO055 needs calibration for accurate readings:

```python
import time
import board
import adafruit_bno055

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

print("BNO055 Calibration Process")
print("Follow these steps:")
print()

while True:
    # Get calibration status
    sys, gyro, accel, mag = sensor.calibration_status
    
    print(f"System: {sys} | Gyro: {gyro} | Accel: {accel} | Mag: {mag}")
    print("(3 = fully calibrated)")
    
    if sys == 3 and gyro == 3 and accel == 3 and mag == 3:
        print("\n✓ Fully calibrated!")
        
        # Save calibration
        calibration = sensor.calibration
        with open('calibration.json', 'w') as f:
            json.dump(calibration, f)
        print("Calibration saved to file")
        break
    
    if accel < 3:
        print("→ Move device through different orientations")
    if gyro < 3:
        print("→ Rotate device slowly")
    if mag < 3:
        print("→ Move in figure-8 pattern")
    
    time.sleep(1)
    print("\n")
```

**Calibration Steps:**
1. **Accelerometer:** Move through 6 positions (face up/down, sides)
2. **Gyroscope:** Rotate slowly in all axes
3. **Magnetometer:** Figure-8 pattern (less important for you)

**Time:** 2-5 minutes

**When to Calibrate:**
- First installation
- After any physical adjustment
- If readings seem inaccurate
- Every few months (drift correction)

### Dynamic Testing

**Test Drive Checklist:**

**Test 1: Gentle Acceleration**
```
Action: Accelerate smoothly from stop to 30 mph
Expected IMU reading: 1-2 m/s² forward
Expected OBD-II: Speed increasing steadily
Expected display: Real-time updates, no lag
```

**Test 2: Gentle Braking**
```
Action: Brake smoothly from 30 mph to stop
Expected IMU reading: -2 to -3 m/s² forward
Expected OBD-II: Speed decreasing steadily
Expected display: Matches physical sensation
```

**Test 3: Cornering**
```
Action: Turn right at 20 mph (normal turn)
Expected IMU reading: 2-3 m/s² lateral (Y-axis)
Expected OBD-II: Speed relatively constant
Expected display: Shows lateral acceleration
```

**Test 4: Bumps/Potholes**
```
Action: Drive over known speed bump or pothole
Expected IMU reading: Spike in Z-axis (up/down)
Expected display: Captures brief spike
Expected: Display unit should not visibly shake
```

**Test 5: Emergency Maneuver**
```
Action: Hard brake from 40 mph (safe conditions!)
Expected IMU reading: -6 to -8 m/s² forward
Expected OBD-II: Rapid speed decrease
Expected: System captures entire event accurately
```

### Troubleshooting

**Problem: IMU readings are noisy**
```
Likely causes:
1. Mount not rigid enough → Add bracing
2. Mounted to flexible part → Relocate to frame
3. Electrical noise → Add shielding, check grounding
4. Sensor defective → Test with known-good sensor
```

**Problem: Display shakes excessively**
```
Likely causes:
1. Insufficient vibration damping → Add foam/rubber
2. Mount resonance frequency → Change damping material
3. Insecure attachment → Strengthen mount
```

**Problem: Readings don't match expected**
```
Likely causes:
1. Axis misalignment → Check orientation
2. Need calibration → Run calibration procedure
3. Mounting location poor → Too far from center of mass
4. Software configuration → Check axis mapping
```

**Problem: System powers off while driving**
```
Likely causes:
1. Insufficient power supply → Use higher amperage
2. Loose connection → Secure all connectors
3. Voltage drop under load → Improve power wiring
4. Overheating → Add cooling/ventilation
```

---

## Maintenance & Long-Term Care

### Regular Checks (Monthly)

- [ ] Verify all mounting screws are tight
- [ ] Check for cracks in mounting bracket/adhesive
- [ ] Inspect cables for wear/chafing
- [ ] Clean display screen
- [ ] Verify IMU calibration status
- [ ] Check SD card has free space

### Seasonal Checks

**Summer (Heat):**
- Check for thermal throttling (Pi 5 can get hot)
- Verify cooling fan functioning
- Check adhesive hasn't softened

**Winter (Cold):**
- Verify display still readable (LCD can slow in cold)
- Check battery drain from OBD-II adapter
- Ensure SD card hasn't corrupted from power cycles

### When to Remount/Recalibrate

**Remount if:**
- Mounting becomes loose or wobbly
- Visible cracks in bracket or base
- Readings become consistently inaccurate
- After any collision or impact

**Recalibrate if:**
- Readings drift over time
- After remounting
- After firmware updates
- Every 3-6 months as preventive maintenance

---

## Bill of Materials - Mounting Hardware

### Option 1: Professional Magnetic Mount (~$50)

```
Component                           Qty    Cost
──────────────────────────────────────────────
Aluminum base plate (3mm)           1      $8
Neodymium magnets N52 (20mm dia)    4      $12
3D printed display enclosure        1      $15
Steel plate (for magnetic attach)   1      $5
M3 screws, washers, nuts (kit)     1      $6
Sorbothane pads (100x100x3mm)      1      $15
Aluminum L-bracket (50x50mm)       1      $5
Cable management (clips, loom)     1      $10
──────────────────────────────────────────────
TOTAL                                      $76
```

### Option 2: Budget VHB Tape Mount (~$25)

```
Component                           Qty    Cost
──────────────────────────────────────────────
3M VHB tape (roll)                  1      $8
Plastic project box (190x110x60mm) 1      $12
EVA foam padding sheets             1      $5
Aluminum L-bracket (50x50mm)       1      $5
M3 screws kit                       1      $4
Cable ties and clips               1      $6
──────────────────────────────────────────────
TOTAL                                      $40
```

### Option 3: RAM Mount System (~$70)

```
Component                           Qty    Cost
──────────────────────────────────────────────
RAM X-Grip holder                   1      $20
RAM double socket arm               1      $15
RAM adhesive base                   1      $15
Custom Pi 5 adapter plate (3D)     1      $10
Aluminum IMU bracket               1      $5
Rubber grommets (vibration)        8      $8
Cable management supplies          1      $10
──────────────────────────────────────────────
TOTAL                                      $83
```

---

## Final Recommendations

### For Your BMW X5 2023 Project

**Recommended Approach:**

**Phase 1: Prototype/Testing (Week 1-2)**
```
Mount: Budget VHB tape mount (~$25)
Location: Center console top
Removable: Yes (with effort)
Purpose: Test functionality and positioning
```

**Phase 2: Permanent Installation (Week 3-4)**
```
Mount: Professional magnetic mount (~$50)
Location: Center console (IMU inside, display on top)
Removable: Yes (quick-release)
Purpose: Final production setup
```

**Key Points:**
1. ✅ Always mount IMU rigidly (no exceptions!)
2. ✅ Isolate display/electronics from vibration
3. ✅ Make display removable for security
4. ✅ Plan cable routing before final installation
5. ✅ Test thoroughly before permanent mounting
6. ✅ Budget extra time for adjustments

**Total Mounting Cost:**
- Prototype: $25-40
- Final: $50-85
- Combined budget: $75-125

**Installation Time:**
- Prototype: 2-4 hours
- Final: 4-8 hours
- Calibration/testing: 2-4 hours
- **Total: 8-16 hours**

---

## Safety & Legal Considerations

**Before Installation:**

1. ✅ Check local laws regarding dashboard-mounted devices
2. ✅ Ensure mount doesn't obstruct:
   - Airbag deployment zones
   - Driver's field of view
   - Vehicle controls
3. ✅ Verify mount can withstand 10G impact (won't become projectile)
4. ✅ Don't interfere with vehicle safety systems
5. ✅ Consider insurance implications of modifications

**BMW X5 Airbag Locations to Avoid:**
- Dashboard (passenger airbag)
- A-pillars (curtain airbags)
- Steering wheel area (driver airbag)
- Side panels (side airbags)

**Safe Zones:**
- ✅ Center console top (between seats)
- ✅ Lower center stack (below airbag deployment)
- ✅ Inside storage compartments (for hidden components)

---

## Resources

**Mounting Hardware Suppliers:**
- McMaster-Carr: https://www.mcmaster.com (quality hardware)
- Amazon: Various mounting solutions
- RAM Mounts: https://www.rammount.com (vehicle mounts)
- Adafruit: https://www.adafruit.com (electronics mounting)

**3D Printing Services:**
- Shapeways: https://www.shapeways.com
- Xometry: https://www.xometry.com  
- Local makerspaces: Often have printers available

**Tools:**
- iFixit toolkit: For electronics disassembly/assembly
- Automotive trim removal tools: For accessing mounting points
- Torque screwdriver set: For proper fastener tightening

---

**Ready to start mounting? Begin with the prototype setup to validate positioning, then upgrade to the professional mount once you're confident in the location!**
