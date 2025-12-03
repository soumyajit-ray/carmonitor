#!/usr/bin/env python3
"""
Simple test script for OBD-II connection.
Run this to verify your Veepeak adapter is working.
"""

import sys
import time
sys.path.insert(0, '/home/rays/carmonitor')

from phase1.obd_reader import OBDReader


def main():
    print("=" * 50)
    print("OBD-II Connection Test")
    print("=" * 50)
    print()
    
    # Create OBD reader
    obd = OBDReader(port='/dev/ttyUSB0')
    
    # Try to connect
    print("Attempting to connect to OBD-II adapter...")
    print("(Make sure car ignition is ON and adapter is plugged in)")
    print()
    
    if not obd.connect(timeout=15):
        print("❌ Failed to connect to OBD-II adapter")
        print()
        print("Troubleshooting:")
        print("1. Check Bluetooth pairing (bluetoothctl)")
        print("2. Verify /dev/rfcomm0 exists")
        print("3. Ensure car ignition is ON")
        print("4. Check adapter is plugged into OBD-II port")
        return 1
    
    print("✅ Connected successfully!")
    print()
    
    # Read data
    print("Reading vehicle data...")
    print("-" * 50)
    
    try:
        for i in range(10):
            data = obd.read_all()
            
            print(f"\rSample {i+1}/10: ", end="")
            print(f"Speed: {data.get('speed_kph', 'N/A'):.1f} km/h | ", end="")
            print(f"RPM: {data.get('rpm', 'N/A'):.0f} | ", end="")
            print(f"Throttle: {data.get('throttle_pct', 'N/A'):.1f}% | ", end="")
            print(f"Accel: {data.get('accel_calculated', 0):.2f} m/s²    ", end="")
            sys.stdout.flush()
            
            time.sleep(0.5)
        
        print("\n")
        print("-" * 50)
        print("✅ Test completed successfully!")
        print()
        print("Your OBD-II adapter is working correctly.")
        print("You can now run the full monitor application.")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during test: {e}")
        return 1
    finally:
        obd.disconnect()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
