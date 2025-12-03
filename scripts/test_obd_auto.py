#!/usr/bin/env python3
"""Test OBD with auto-detection for BLE adapters."""

import obd
import time

print("Scanning for OBD adapters...")
print("This may take 10-15 seconds...\n")

# Try auto-detection
try:
    connection = obd.OBD()  # Auto-detect
    
    if connection.is_connected():
        print("✅ Connected to OBD adapter!")
        print(f"Port: {connection.port_name()}")
        print(f"Protocol: {connection.protocol_name()}")
        print()
        
        # Try reading some data
        print("Reading vehicle data...")
        for i in range(5):
            speed = connection.query(obd.commands.SPEED)
            rpm = connection.query(obd.commands.RPM)
            
            print(f"Sample {i+1}: Speed={speed.value if not speed.is_null() else 'N/A'}, RPM={rpm.value if not rpm.is_null() else 'N/A'}")
            time.sleep(1)
        
        connection.close()
        print("\n✅ Test successful!")
    else:
        print("❌ No OBD adapter found")
        print("\nTroubleshooting:")
        print("1. Make sure car ignition is ON")
        print("2. Check adapter is plugged in firmly")
        print("3. Wait 30 seconds after plugging in adapter")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
