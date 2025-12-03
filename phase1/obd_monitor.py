#!/usr/bin/env python3
"""
Phase 1 OBD-II Monitor - Console Version
Main application for driver behavior monitoring using OBD-II data.
"""

import sys
import time
import signal
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.config import Config
from common.logger import TripLogger
from common.scoring import DriverScorer
from phase1.obd_reader import OBDReader


class Phase1Monitor:
    """Main monitor application for Phase 1."""
    
    def __init__(self):
        """Initialize the monitor."""
        # Load configuration
        self.config = Config(phase=1)
        
        # Initialize components
        self.obd = OBDReader(
            port=self.config.get('obd.port'),
            baudrate=self.config.get('obd.baudrate')
        )
        
        self.logger = TripLogger(
            log_dir=self.config.log_directory,
            phase=1
        )
        
        self.scorer = DriverScorer(
            config=self.config.get_section('scoring')
        )
        
        self.running = False
        self.trip_active = False
    
    def start(self) -> bool:
        """
        Start the monitor.
        
        Returns:
            True if started successfully
        """
        print("="  * 60)
        print("BMW X5 Driver Behavior Monitor - Phase 1")
        print("OBD-II Based Monitoring")
        print("=" * 60)
        print()
        
        # Connect to OBD-II
        print("Connecting to OBD-II adapter...")
        if not self.obd.connect(timeout=15):
            print("❌ Failed to connect to OBD-II adapter")
            return False
        
        print("✅ OBD-II connected")
        print()
        
        self.running = True
        return True
    
    def start_trip(self):
        """Start a new trip."""
        if self.trip_active:
            print("Trip already active!")
            return
        
        trip_name = time.strftime('trip_%Y%m%d_%H%M%S')
        self.logger.start_trip(trip_name)
        self.scorer.reset()
        self.trip_active = True
        
        print("\n" + "=" * 60)
        print("🚗 TRIP STARTED")
        print("=" * 60)
        print()
    
    def stop_trip(self):
        """Stop current trip."""
        if not self.trip_active:
            return
        
        summary = self.logger.end_trip()
        score_summary = self.scorer.get_summary()
        self.trip_active = False
        
        print("\n" + "=" * 60)
        print("🏁 TRIP ENDED")
        print("=" * 60)
        print(f"Duration: {summary['duration_seconds']:.1f} seconds")
        print(f"Data points: {summary['data_points']}")
        print(f"Log file: {summary['file']}")
        print()
        print("DRIVING SCORE:")
        print(f"  Final Score: {score_summary['current_score']:.1f}/100 ({self.scorer.get_grade()})")
        print(f"  Average Score: {score_summary['average_score']:.1f}/100")
        print()
        print("EVENTS:")
        print(f"  Harsh Braking: {score_summary['harsh_braking_events']}")
        print(f"  Aggressive Acceleration: {score_summary['aggressive_accel_events']}")
        print(f"  Speeding: {score_summary['speeding_events']}")
        print("=" * 60)
        print()
    
    def run(self):
        """Main monitoring loop."""
        if not self.start():
            return 1
        
        # Setup signal handler for clean shutdown
        def signal_handler(sig, frame):
            print("\n\nShutting down...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        
        print("Commands:")
        print("  Press 's' + ENTER to start trip")
        print("  Press 'x' + ENTER to stop trip")
        print("  Press 'q' + ENTER to quit")
        print()
        
        # Start async OBD reading
        self.obd.start_async_reading(update_rate=0.1)
        
        last_display_update = time.time()
        display_interval = 1.0  # Update display every second
        
        try:
            while self.running:
                # Get latest data
                data = self.obd.get_latest_data()
                
                if self.trip_active and data:
                    # Update score
                    score, event_type = self.scorer.update(
                        speed_kph=data.get('speed_kph', 0),
                        accel=data.get('accel_calculated', 0)
                    )
                    
                    # Add to data
                    data['event_type'] = event_type
                    data['score'] = score
                    
                    # Log data
                    self.logger.log_data(data)
                
                # Update display
                current_time = time.time()
                if current_time - last_display_update >= display_interval:
                    self.display_status(data)
                    last_display_update = current_time
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        finally:
            self.shutdown()
        
        return 0
    
    def display_status(self, data: dict):
        """
        Display current status.
        
        Args:
            data: Current vehicle data
        """
        # Clear screen (simple version)
        print("\033[2J\033[H", end="")
        
        print("=" * 60)
        print("BMW X5 Driver Behavior Monitor - Phase 1")
        print("=" * 60)
        print()
        
        if self.trip_active:
            print(f"🚗 TRIP ACTIVE - Duration: {self.logger.get_trip_duration():.0f}s")
        else:
            print("⏸️  NO ACTIVE TRIP - Press 's' to start")
        
        print()
        print("VEHICLE DATA:")
        print(f"  Speed:        {data.get('speed_kph', 0):.1f} km/h")
        print(f"  RPM:          {data.get('rpm', 0):.0f}")
        print(f"  Throttle:     {data.get('throttle_pct', 0):.1f}%")
        print(f"  Engine Load:  {data.get('engine_load', 0):.1f}%")
        print(f"  Acceleration: {data.get('accel_calculated', 0):.2f} m/s²")
        
        if self.trip_active:
            print()
            print("DRIVING SCORE:")
            print(f"  Current: {self.scorer.current_score:.1f}/100 ({self.scorer.get_grade()})")
            print(f"  Events: {self.scorer.harsh_brake_count} harsh brakes, ", end="")
            print(f"{self.scorer.aggressive_accel_count} aggressive accels")
            print(f"  Last Event: {data.get('event_type', 'normal')}")
        
        print()
        print("Commands: [s]tart trip | [x] stop trip | [q]uit")
        print("=" * 60)
    
    def shutdown(self):
        """Clean shutdown."""
        if self.trip_active:
            self.stop_trip()
        
        self.obd.stop_async_reading()
        self.obd.disconnect()
        print("Monitor shutdown complete")


def main():
    """Main entry point."""
    monitor = Phase1Monitor()
    return monitor.run()


if __name__ == '__main__':
    sys.exit(main())
