#!/bin/bash
# Auto-start script for BMW X5 Car Monitor

# Wait for display to be ready
sleep 5

# Wait for OBD device (up to 30 seconds)
echo "Waiting for OBD device..."
for i in {1..30}; do
    if [ -e /dev/ttyUSB0 ]; then
        echo "OBD device found!"
        break
    fi
    sleep 1
done

# Set display
export DISPLAY=:0

# Change to project directory
cd /home/rays/carmonitor

# Start the GUI
python3 phase1/obd_monitor_touch.py > /tmp/carmonitor_autostart.log 2>&1 &

echo "Car Monitor started at $(date)" >> /tmp/carmonitor_autostart.log
