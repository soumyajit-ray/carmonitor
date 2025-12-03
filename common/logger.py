"""
Data logging system for Car Monitor project.
Handles CSV logging of trip data and session management.
"""

import os
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class TripLogger:
    """Logger for trip data with CSV export."""
    
    def __init__(self, log_dir: str, phase: int = 1):
        """
        Initialize trip logger.
        
        Args:
            log_dir: Directory to store log files
            phase: Phase number (determines which fields to log)
        """
        self.log_dir = Path(log_dir)
        self.phase = phase
        self.current_file = None
        self.csv_writer = None
        self.file_handle = None
        self.trip_start_time = None
        self.row_count = 0
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Define fields based on phase
        self.fieldnames = self._get_fieldnames()
    
    def _get_fieldnames(self) -> List[str]:
        """Get CSV field names based on phase."""
        # Phase 1: OBD-II only
        phase1_fields = [
            'timestamp',
            'speed_kph',
            'throttle_pct',
            'rpm',
            'engine_load',
            'accel_calculated',
            'event_type',
            'score'
        ]
        
        # Phase 2: + IMU + GPS
        phase2_fields = phase1_fields + [
            'accel_x',
            'accel_y',
            'accel_z',
            'jerk',
            'latitude',
            'longitude',
            'gps_speed',
            'gps_bearing'
        ]
        
        # Phase 3: + Lane Detection
        phase3_fields = phase2_fields + [
            'lane_center_offset',
            'lane_confidence',
            'lane_status',
            'video_frame'
        ]
        
        if self.phase == 1:
            return phase1_fields
        elif self.phase == 2:
            return phase2_fields
        else:
            return phase3_fields
    
    def start_trip(self, trip_name: Optional[str] = None) -> str:
        """
        Start a new trip logging session.
        
        Args:
            trip_name: Optional custom trip name. If None, uses timestamp.
            
        Returns:
            Path to log file
        """
        if self.file_handle:
            self.end_trip()
        
        self.trip_start_time = datetime.now()
        
        if trip_name is None:
            trip_name = self.trip_start_time.strftime('trip_%Y%m%d_%H%M%S')
        
        self.current_file = self.log_dir / f"{trip_name}.csv"
        self.file_handle = open(self.current_file, 'w', newline='')
        self.csv_writer = csv.DictWriter(
            self.file_handle,
            fieldnames=self.fieldnames
        )
        self.csv_writer.writeheader()
        self.row_count = 0
        
        print(f"Started trip logging: {self.current_file}")
        return str(self.current_file)
    
    def log_data(self, data: Dict[str, Any]):
        """
        Log a data point to the current trip.
        
        Args:
            data: Dictionary with field values
        """
        if not self.csv_writer:
            raise RuntimeError("No active trip. Call start_trip() first.")
        
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        # Filter to only include defined fieldnames
        filtered_data = {k: v for k, v in data.items() if k in self.fieldnames}
        
        self.csv_writer.writerow(filtered_data)
        self.row_count += 1
        
        # Flush every 10 rows to ensure data isn't lost
        if self.row_count % 10 == 0:
            self.file_handle.flush()
    
    def end_trip(self) -> Dict[str, Any]:
        """
        End current trip logging session.
        
        Returns:
            Trip summary statistics
        """
        if not self.file_handle:
            return {}
        
        trip_end_time = datetime.now()
        duration = (trip_end_time - self.trip_start_time).total_seconds()
        
        summary = {
            'file': str(self.current_file),
            'start_time': self.trip_start_time.isoformat(),
            'end_time': trip_end_time.isoformat(),
            'duration_seconds': duration,
            'data_points': self.row_count
        }
        
        self.file_handle.close()
        self.file_handle = None
        self.csv_writer = None
        self.current_file = None
        self.row_count = 0
        
        print(f"Trip ended. Duration: {duration:.1f}s, Data points: {summary['data_points']}")
        return summary
    
    def is_logging(self) -> bool:
        """Check if currently logging a trip."""
        return self.file_handle is not None
    
    def get_trip_duration(self) -> float:
        """
        Get current trip duration in seconds.
        
        Returns:
            Duration in seconds, or 0 if no active trip
        """
        if not self.trip_start_time:
            return 0.0
        return (datetime.now() - self.trip_start_time).total_seconds()
    
    def __del__(self):
        """Ensure file is closed on cleanup."""
        if self.file_handle:
            self.end_trip()


class RealTimeLogger:
    """Lightweight real-time logger for high-frequency data."""
    
    def __init__(self, log_file: str, buffer_size: int = 100):
        """
        Initialize real-time logger.
        
        Args:
            log_file: Path to log file
            buffer_size: Number of entries to buffer before flushing
        """
        self.log_file = Path(log_file)
        self.buffer_size = buffer_size
        self.buffer = []
        self.file_handle = None
        
        # Ensure parent directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, message: str):
        """
        Log a message.
        
        Args:
            message: Message to log
        """
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        self.buffer.append(log_entry)
        
        if len(self.buffer) >= self.buffer_size:
            self.flush()
    
    def flush(self):
        """Flush buffer to file."""
        if not self.buffer:
            return
        
        with open(self.log_file, 'a') as f:
            f.writelines(self.buffer)
        
        self.buffer.clear()
    
    def __del__(self):
        """Flush remaining buffer on cleanup."""
        self.flush()
