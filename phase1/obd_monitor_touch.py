#!/usr/bin/env python3
import sys, tkinter as tk
from datetime import datetime
import threading
import time
import math

sys.path.insert(0, "/home/rays/carmonitor")
from phase1.obd_reader import OBDReader
from common.config import Config
from common.logger import TripLogger
from common.scoring import DriverScorer

class AccelGauge(tk.Canvas):
    def __init__(self, parent, width=220, height=160):
        super().__init__(parent, width=width, height=height, bg="black", highlightthickness=0)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2 + 10
        self.radius = 70
        
        # Thresholds
        self.harsh_brake = -5.0
        self.aggressive_accel = 3.0
        self.min_val = -8.0
        self.max_val = 6.0
        
        self.draw_static()
        
    def draw_static(self):
        """Draw the static parts of the gauge"""
        # Calculate angles for zones
        harsh_angle = self.value_to_angle(self.harsh_brake)  # ~146° for -5.0
        accel_angle = self.value_to_angle(self.aggressive_accel)  # ~45° for +3.0

        # Draw three arc segments for top semicircle (0° to 180°)
        arc_width = 25

        # Right red zone (aggressive acceleration): 0° to accel_angle
        self.create_arc(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            start=0, extent=accel_angle, outline="#e74c3c",
            style=tk.ARC, width=arc_width
        )

        # Green zone (safe range): accel_angle to harsh_angle
        self.create_arc(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            start=accel_angle, extent=harsh_angle - accel_angle,
            outline="#2ecc71", style=tk.ARC, width=arc_width
        )

        # Left red zone (harsh braking): harsh_angle to 180°
        self.create_arc(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            start=harsh_angle, extent=180 - harsh_angle,
            outline="#e74c3c", style=tk.ARC, width=arc_width
        )
        
        # Draw center circle
        center_r = 10
        self.create_oval(
            self.center_x - center_r, self.center_y - center_r,
            self.center_x + center_r, self.center_y + center_r,
            fill="#2c3e50", outline="white", width=2
        )
        
        # Draw threshold markers
        for val in [self.harsh_brake, 0, self.aggressive_accel]:
            angle = self.value_to_angle(val)
            angle_rad = math.radians(angle)
            x1 = self.center_x + (self.radius - 12) * math.cos(angle_rad)
            y1 = self.center_y - (self.radius - 12) * math.sin(angle_rad)
            x2 = self.center_x + (self.radius + 5) * math.cos(angle_rad)
            y2 = self.center_y - (self.radius + 5) * math.sin(angle_rad)
            self.create_line(x1, y1, x2, y2, fill="white", width=2)
        
        # Labels
        # Left label (harsh brake)
        angle_rad = math.radians(self.value_to_angle(self.harsh_brake))
        x = self.center_x + (self.radius + 20) * math.cos(angle_rad)
        y = self.center_y - (self.radius + 20) * math.sin(angle_rad)
        self.create_text(x, y, text=str(int(self.harsh_brake)), 
                        fill="white", font=("Helvetica", 9, "bold"))
        
        # Top label (0)
        self.create_text(self.center_x, self.center_y - self.radius - 18, text="0", 
                        fill="white", font=("Helvetica", 10, "bold"))
        
        # Right label (aggressive accel)
        angle_rad = math.radians(self.value_to_angle(self.aggressive_accel))
        x = self.center_x + (self.radius + 20) * math.cos(angle_rad)
        y = self.center_y - (self.radius + 20) * math.sin(angle_rad)
        self.create_text(x, y, text=f"+{int(self.aggressive_accel)}", 
                        fill="white", font=("Helvetica", 9, "bold"))
        
        self.create_text(self.center_x, 8, text="ACCEL (m/s²)", 
                        fill="gray", font=("Helvetica", 9, "bold"))
        
        # Needle (will be updated)
        self.needle = None
        self.value_text = self.create_text(self.center_x, self.height - 15, 
                                           text="0.0", fill="white", 
                                           font=("Helvetica", 14, "bold"))
    
    def value_to_angle(self, value):
        """Convert acceleration value to angle (90 degrees = straight up at 0)"""
        # Map so that 0 is exactly at 90 degrees (straight up/12 o'clock)
        # Negative values (braking) go left (90 to 180 degrees)
        # Positive values (accel) go right (90 to 0 degrees)
        if value <= 0:
            # Braking side: min_val -> 180°, 0 -> 90°
            if self.min_val != 0:
                normalized = (value - self.min_val) / (0 - self.min_val)
                angle = 180 - (normalized * 90)  # Maps from 180 to 90
            else:
                angle = 90
        else:
            # Acceleration side: 0 -> 90°, max_val -> 0°
            if self.max_val != 0:
                normalized = value / self.max_val
                angle = 90 - (normalized * 90)  # Maps from 90 to 0
            else:
                angle = 90
        return angle
    
    def update_needle(self, value):
        """Update the needle position"""
        # Clamp value
        value = max(self.min_val, min(self.max_val, value))
        
        # Delete old needle
        if self.needle:
            self.delete(self.needle)
        
        # Calculate needle position
        angle = self.value_to_angle(value)
        angle_rad = math.radians(angle)
        end_x = self.center_x + (self.radius - 15) * math.cos(angle_rad)
        end_y = self.center_y - (self.radius - 15) * math.sin(angle_rad)
        
        # Draw needle
        self.needle = self.create_line(
            self.center_x, self.center_y, end_x, end_y,
            fill="#f39c12", width=4, arrow=tk.LAST, arrowshape=(10, 12, 4)
        )
        
        # Update value text
        color = "#2ecc71" if self.harsh_brake <= value <= self.aggressive_accel else "#e74c3c"
        self.itemconfig(self.value_text, text=f"{value:.1f}", fill=color)


class AutoConnectGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x480")
        self.root.configure(bg="black")
        
        self.config = Config("/home/rays/carmonitor/config/phase1_config.yaml")
        self.obd = None
        self.logger = TripLogger(log_dir=self.config.get("logging.directory"))
        cfg = {"harsh_brake_threshold": self.config.get("scoring.harsh_brake_threshold"),
               "aggressive_accel_threshold": self.config.get("scoring.aggressive_accel_threshold"),
               "speeding_threshold": self.config.get("scoring.speeding_threshold")}
        self.scorer = DriverScorer(config=cfg)
        
        self.trip_active = False
        self.connected = False
        self.last_data = {}
        self.running = True
        self.connection_attempts = 0
        
        self.create_widgets()
        threading.Thread(target=self.connection_monitor, daemon=True).start()
        self.update_display()
    
    def create_widgets(self):
        # BUTTONS AT TOP - Reduced height to 60px
        btns = tk.Frame(self.root, bg="#2c3e50", height=60)
        btns.pack(side=tk.TOP, fill=tk.X)
        btns.pack_propagate(False)
        
        tk.Label(btns, text="BMW X5", font=("Helvetica", 12, "bold"), 
                bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=10)
        
        self.start_btn = tk.Button(btns, text="START", font=("Helvetica", 16, "bold"), 
                                   bg="#2ecc71", fg="white", command=self.start_trip, 
                                   width=7, height=1)
        self.start_btn.pack(side=tk.LEFT, padx=8, pady=10)
        
        self.stop_btn = tk.Button(btns, text="STOP", font=("Helvetica", 16, "bold"),
                                  bg="#e74c3c", fg="white", command=self.stop_trip, 
                                  width=7, height=1, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(btns, text="QUIT", font=("Helvetica", 16, "bold"),
                 bg="#95a5a6", fg="white", command=self.quit_app, 
                 width=5, height=1).pack(side=tk.RIGHT, padx=8, pady=10)
        
        self.status = tk.Label(btns, text="Connecting...", font=("Helvetica", 10), 
                              bg="#2c3e50", fg="#f39c12")
        self.status.pack(side=tk.RIGHT, padx=10)
        
        # Main area
        main = tk.Frame(self.root, bg="black")
        main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left: Speed + RPM/Throttle
        left = tk.Frame(main, bg="black")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.speed = tk.Label(left, text="--", font=("Helvetica", 60, "bold"), 
                             bg="black", fg="white")
        self.speed.pack()
        tk.Label(left, text="km/h", font=("Helvetica", 14), 
                bg="black", fg="gray").pack()
        
        self.rpm = tk.Label(left, text="RPM: --", font=("Helvetica", 16), 
                           bg="black", fg="white")
        self.rpm.pack(pady=3)
        self.throttle = tk.Label(left, text="Throttle: --", font=("Helvetica", 16), 
                                bg="black", fg="white")
        self.throttle.pack()
        
        # Center: Acceleration Gauge
        center = tk.Frame(main, bg="black")
        center.pack(side=tk.LEFT, padx=5)
        
        self.accel_gauge = AccelGauge(center)
        self.accel_gauge.pack()
        
        # Right: Score panel
        right = tk.Frame(main, bg="#34495e", width=200)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)
        
        self.trip_lbl = tk.Label(right, text="READY", font=("Helvetica", 12, "bold"), 
                                bg="#34495e", fg="#f39c12")
        self.trip_lbl.pack(pady=8)
        
        self.score_lbl = tk.Label(right, text="--", font=("Helvetica", 50, "bold"), 
                                 bg="#34495e", fg="#2ecc71")
        self.score_lbl.pack(pady=5)
        self.grade = tk.Label(right, text="Grade: --", font=("Helvetica", 14), 
                             bg="#34495e", fg="white")
        self.grade.pack()
        self.events = tk.Label(right, text="Events: 0", font=("Helvetica", 11), 
                              bg="#34495e", fg="gray")
        self.events.pack(pady=8)
    
    def connection_monitor(self):
        """Continuously monitor and attempt OBD connection"""
        while self.running:
            if not self.connected:
                self.connection_attempts += 1
                status_msg = f"Connecting... ({self.connection_attempts})"
                self.status.config(text=status_msg, fg="#f39c12")
                
                try:
                    if self.obd is None:
                        self.obd = OBDReader(
                            port=self.config.get("obd.port"),
                            baudrate=self.config.get("obd.baudrate")
                        )
                    
                    if self.obd.connect(timeout=5):
                        self.connected = True
                        self.obd.start_async_reading(update_rate=0.1)
                        self.status.config(text="Connected ●", fg="#2ecc71")
                        self.start_btn.config(state=tk.NORMAL)
                    else:
                        time.sleep(3)
                except Exception as e:
                    time.sleep(3)
            else:
                time.sleep(5)
    
    def start_trip(self):
        if not self.trip_active and self.connected:
            self.logger.start_trip(datetime.now().strftime("trip_%Y%m%d_%H%M%S"))
            self.scorer.reset()
            self.trip_active = True
            self.trip_lbl.config(text="RECORDING", fg="#2ecc71")
            self.start_btn.config(state=tk.DISABLED, bg="gray")
            self.stop_btn.config(state=tk.NORMAL, bg="#e74c3c")
    
    def stop_trip(self):
        if self.trip_active:
            self.logger.end_trip()
            self.trip_active = False
            self.trip_lbl.config(text="STOPPED", fg="#f39c12")
            self.start_btn.config(state=tk.NORMAL, bg="#2ecc71")
            self.stop_btn.config(state=tk.DISABLED, bg="gray")
    
    def update_display(self):
        if not self.running:
            return
        
        if self.connected and self.obd:
            try:
                self.last_data = self.obd.get_latest_data()
                spd = self.last_data.get("speed_kph", 0) or 0
                rpm = self.last_data.get("rpm", 0) or 0
                thr = self.last_data.get("throttle_pct", 0) or 0
                accel = self.last_data.get("accel_calculated", 0) or 0
                
                self.speed.config(text=f"{spd:.0f}")
                self.rpm.config(text=f"RPM: {rpm:.0f}")
                self.throttle.config(text=f"Throttle: {thr:.0f}%")
                
                # Update acceleration gauge
                self.accel_gauge.update_needle(accel)
                
                if self.trip_active and self.last_data:
                    score, evt = self.scorer.update(speed_kph=spd, accel=accel)
                    grade = self.scorer.get_grade()
                    self.score_lbl.config(text=f"{score:.0f}")
                    self.grade.config(text=f"Grade: {grade}")
                    color = "#2ecc71" if grade in ["A","B"] else "#f39c12" if grade=="C" else "#e74c3c"
                    self.score_lbl.config(fg=color)
                    events_total = self.scorer.harsh_brake_count + self.scorer.aggressive_accel_count
                    self.events.config(text=f"Events: {events_total}")
                    self.logger.log_data({**self.last_data, "score": score, "event_type": evt or ""})
            except Exception as e:
                pass
        else:
            # Not connected - show 0 on gauge
            self.accel_gauge.update_needle(0)
        
        self.root.after(100, self.update_display)
    
    def quit_app(self):
        self.running = False
        if self.trip_active:
            self.stop_trip()
        if self.connected and self.obd:
            self.obd.disconnect()
        self.root.quit()

root = tk.Tk()
app = AutoConnectGUI(root)
root.mainloop()
