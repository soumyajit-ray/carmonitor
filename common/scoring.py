"""
Driver behavior scoring algorithms for Car Monitor project.
Calculates scores based on acceleration, braking, and driving patterns.
"""

from typing import List, Dict, Tuple
from collections import deque
import time


class DriverScorer:
    """Calculate driver behavior scores based on driving metrics."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize driver scorer.
        
        Args:
            config: Configuration dictionary with thresholds
        """
        # Default thresholds (can be overridden)
        self.harsh_brake_threshold = -5.0  # m/s²
        self.aggressive_accel_threshold = 3.0  # m/s²
        self.smooth_jerk_threshold = 3.0  # m/s³
        self.speeding_threshold = 120  # kph
        
        if config:
            self.harsh_brake_threshold = config.get('harsh_brake_threshold', self.harsh_brake_threshold)
            self.aggressive_accel_threshold = config.get('aggressive_accel_threshold', self.aggressive_accel_threshold)
            self.speeding_threshold = config.get('speeding_threshold', self.speeding_threshold)
        
        # Event counters
        self.harsh_brake_count = 0
        self.aggressive_accel_count = 0
        self.speeding_count = 0
        
        # Score tracking
        self.current_score = 100.0
        self.score_history = deque(maxlen=100)
        
        # Time tracking
        self.start_time = time.time()
        self.total_distance = 0.0
    
    def reset(self):
        """Reset all counters and scores."""
        self.harsh_brake_count = 0
        self.aggressive_accel_count = 0
        self.speeding_count = 0
        self.current_score = 100.0
        self.score_history.clear()
        self.start_time = time.time()
        self.total_distance = 0.0
    
    def update(self, speed_kph: float, accel: float, **kwargs) -> Tuple[float, str]:
        """
        Update score based on current driving metrics.
        
        Args:
            speed_kph: Current speed in km/h
            accel: Current acceleration in m/s²
            **kwargs: Additional metrics (throttle, jerk, etc.)
            
        Returns:
            Tuple of (current_score, event_type)
        """
        event_type = 'normal'
        penalty = 0.0
        
        # Check for harsh braking
        if accel < self.harsh_brake_threshold:
            self.harsh_brake_count += 1
            event_type = 'harsh_brake'
            penalty = 2.0
        
        # Check for aggressive acceleration
        elif accel > self.aggressive_accel_threshold:
            self.aggressive_accel_count += 1
            event_type = 'aggressive_accel'
            penalty = 1.5
        
        # Check for speeding
        if speed_kph > self.speeding_threshold:
            self.speeding_count += 1
            if event_type == 'normal':
                event_type = 'speeding'
            penalty += 0.5
        
        # Apply penalty
        self.current_score = max(0.0, self.current_score - penalty)
        
        # Gradual score recovery for good driving
        if event_type == 'normal' and self.current_score < 100.0:
            self.current_score = min(100.0, self.current_score + 0.01)
        
        self.score_history.append(self.current_score)
        
        return self.current_score, event_type
    
    def get_summary(self) -> Dict:
        """
        Get scoring summary.
        
        Returns:
            Dictionary with score summary and statistics
        """
        duration = time.time() - self.start_time
        
        return {
            'current_score': self.current_score,
            'average_score': sum(self.score_history) / len(self.score_history) if self.score_history else 100.0,
            'harsh_braking_events': self.harsh_brake_count,
            'aggressive_accel_events': self.aggressive_accel_count,
            'speeding_events': self.speeding_count,
            'trip_duration_sec': duration,
            'total_events': self.harsh_brake_count + self.aggressive_accel_count + self.speeding_count
        }
    
    def get_grade(self) -> str:
        """
        Get letter grade based on current score.
        
        Returns:
            Letter grade (A+ to F)
        """
        score = self.current_score
        
        if score >= 95:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 85:
            return 'B+'
        elif score >= 80:
            return 'B'
        elif score >= 75:
            return 'C+'
        elif score >= 70:
            return 'C'
        elif score >= 65:
            return 'D'
        else:
            return 'F'


def calculate_acceleration(speed_history: List[Tuple[float, float]]) -> float:
    """
    Calculate acceleration from speed history.
    
    Args:
        speed_history: List of (timestamp, speed_kph) tuples
        
    Returns:
        Acceleration in m/s²
    """
    if len(speed_history) < 2:
        return 0.0
    
    # Get last two data points
    time1, speed1 = speed_history[-2]
    time2, speed2 = speed_history[-1]
    
    # Convert km/h to m/s
    speed1_ms = speed1 / 3.6
    speed2_ms = speed2 / 3.6
    
    # Calculate acceleration
    dt = time2 - time1
    if dt > 0:
        accel = (speed2_ms - speed1_ms) / dt
        return accel
    
    return 0.0


def calculate_jerk(accel_history: List[Tuple[float, float]]) -> float:
    """
    Calculate jerk (rate of change of acceleration).
    
    Args:
        accel_history: List of (timestamp, acceleration) tuples
        
    Returns:
        Jerk in m/s³
    """
    if len(accel_history) < 2:
        return 0.0
    
    time1, accel1 = accel_history[-2]
    time2, accel2 = accel_history[-1]
    
    dt = time2 - time1
    if dt > 0:
        jerk = (accel2 - accel1) / dt
        return jerk
    
    return 0.0
