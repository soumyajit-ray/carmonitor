"""
OBD-II Reader for Car Monitor - Phase 1.
Interfaces with Veepeak OBDCheck BLE adapter to read vehicle data.
"""

import obd
import time
from typing import Dict, Optional, List, Tuple
from collections import deque
from threading import Thread, Lock, Event


class OBDReader:
    """OBD-II interface for reading vehicle data."""
    
    def __init__(self, port: str = '/dev/rfcomm0', baudrate: int = 38400):
        """
        Initialize OBD-II reader.
        
        Args:
            port: Serial port for OBD adapter
            baudrate: Communication baudrate
        """
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        self.is_connected = False
        
        # Data storage
        self.speed_history = deque(maxlen=10)  # (timestamp, speed) pairs
        self.latest_data = {}
        self.data_lock = Lock()
        
        # Async reading
        self.async_thread = None
        self.stop_event = Event()
        self.update_rate = 0.1  # 10 Hz
    
    def connect(self, timeout: int = 10) -> bool:
        """
        Connect to OBD-II adapter.
        
        Args:
            timeout: Connection timeout in seconds
            
        Returns:
            True if connected successfully
        """
        try:
            print(f"Connecting to OBD-II adapter on {self.port}...")
            self.connection = obd.OBD(self.port, baudrate=self.baudrate, timeout=timeout)
            
            if self.connection.is_connected():
                self.is_connected = True
                print("OBD-II connection established!")
                print(f"Protocol: {self.connection.protocol_name()}")
                print(f"Vehicle: {self.connection.protocol_id()}")
                return True
            else:
                print("Failed to connect to OBD-II adapter")
                return False
                
        except Exception as e:
            print(f"Error connecting to OBD-II: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from OBD-II adapter."""
        if self.async_thread:
            self.stop_async_reading()
        
        if self.connection:
            self.connection.close()
            self.is_connected = False
            print("OBD-II disconnected")
    
    def read_speed(self) -> Optional[float]:
        """
        Read vehicle speed.
        
        Returns:
            Speed in km/h or None if failed
        """
        if not self.is_connected:
            return None
        
        try:
            response = self.connection.query(obd.commands.SPEED)
            if not response.is_null():
                return response.value.magnitude
        except:
            pass
        return None
    
    def read_rpm(self) -> Optional[float]:
        """
        Read engine RPM.
        
        Returns:
            RPM or None if failed
        """
        if not self.is_connected:
            return None
        
        try:
            response = self.connection.query(obd.commands.RPM)
            if not response.is_null():
                return response.value.magnitude
        except:
            pass
        return None
    
    def read_throttle(self) -> Optional[float]:
        """
        Read throttle position.
        
        Returns:
            Throttle percentage (0-100) or None if failed
        """
        if not self.is_connected:
            return None
        
        try:
            response = self.connection.query(obd.commands.THROTTLE_POS)
            if not response.is_null():
                return response.value.magnitude
        except:
            pass
        return None
    
    def read_engine_load(self) -> Optional[float]:
        """
        Read calculated engine load.
        
        Returns:
            Engine load percentage (0-100) or None if failed
        """
        if not self.is_connected:
            return None
        
        try:
            response = self.connection.query(obd.commands.ENGINE_LOAD)
            if not response.is_null():
                return response.value.magnitude
        except:
            pass
        return None
    
    def read_all(self) -> Dict:
        """
        Read all available OBD-II data.
        
        Returns:
            Dictionary with all current values
        """
        data = {
            'timestamp': time.time(),
            'speed_kph': self.read_speed(),
            'rpm': self.read_rpm(),
            'throttle_pct': self.read_throttle(),
            'engine_load': self.read_engine_load()
        }
        
        # Calculate acceleration from speed history
        if data['speed_kph'] is not None:
            self.speed_history.append((data['timestamp'], data['speed_kph']))
            data['accel_calculated'] = self.calculate_acceleration()
        else:
            data['accel_calculated'] = None
        
        with self.data_lock:
            self.latest_data = data
        
        return data
    
    def calculate_acceleration(self) -> float:
        """
        Calculate acceleration from speed history.
        
        Returns:
            Acceleration in m/s²
        """
        if len(self.speed_history) < 2:
            return 0.0
        
        # Get last two data points
        time1, speed1 = self.speed_history[-2]
        time2, speed2 = self.speed_history[-1]
        
        # Convert km/h to m/s
        speed1_ms = speed1 / 3.6
        speed2_ms = speed2 / 3.6
        
        # Calculate acceleration
        dt = time2 - time1
        if dt > 0:
            accel = (speed2_ms - speed1_ms) / dt
            return accel
        
        return 0.0
    
    def get_latest_data(self) -> Dict:
        """
        Get latest data (thread-safe).
        
        Returns:
            Dictionary with latest data
        """
        with self.data_lock:
            return self.latest_data.copy()
    
    def start_async_reading(self, update_rate: float = 0.1):
        """
        Start asynchronous data reading in background thread.
        
        Args:
            update_rate: Update interval in seconds (default 10 Hz)
        """
        if self.async_thread and self.async_thread.is_alive():
            print("Async reading already running")
            return
        
        self.update_rate = update_rate
        self.stop_event.clear()
        self.async_thread = Thread(target=self._async_read_loop, daemon=True)
        self.async_thread.start()
        print(f"Started async OBD-II reading at {1/update_rate:.1f} Hz")
    
    def stop_async_reading(self):
        """Stop asynchronous data reading."""
        if self.async_thread:
            self.stop_event.set()
            self.async_thread.join(timeout=2.0)
            print("Stopped async OBD-II reading")
    
    def _async_read_loop(self):
        """Background thread loop for reading OBD-II data."""
        while not self.stop_event.is_set():
            try:
                self.read_all()
            except Exception as e:
                print(f"Error in async read: {e}")
            
            time.sleep(self.update_rate)
    
    def is_vehicle_moving(self, threshold_kph: float = 1.0) -> bool:
        """
        Check if vehicle is moving.
        
        Args:
            threshold_kph: Minimum speed to consider moving
            
        Returns:
            True if vehicle is moving
        """
        data = self.get_latest_data()
        speed = data.get('speed_kph')
        return speed is not None and speed > threshold_kph
    
    def __repr__(self) -> str:
        status = "connected" if self.is_connected else "disconnected"
        return f"OBDReader(port={self.port}, status={status})"
