#!/usr/bin/env python3
import sys, tkinter as tk
from datetime import datetime
import threading
import time

sys.path.insert(0, "/home/rays/carmonitor")
from phase1.obd_reader import OBDReader
from common.config import Config
from common.logger import TripLogger
from common.scoring import DriverScorer

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
        # BUTTONS AT TOP
        btns = tk.Frame(self.root, bg="#2c3e50", height=70)
        btns.pack(side=tk.TOP, fill=tk.X)
        btns.pack_propagate(False)
        
        tk.Label(btns, text="BMW X5", font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=10)
        
        self.start_btn = tk.Button(btns, text="START", font=("Helvetica", 18, "bold"), 
                                   bg="#2ecc71", fg="white", command=self.start_trip, width=8, height=1)
        self.start_btn.pack(side=tk.LEFT, padx=10, pady=15)
        
        self.stop_btn = tk.Button(btns, text="STOP", font=("Helvetica", 18, "bold"),
                                  bg="#e74c3c", fg="white", command=self.stop_trip, width=8, height=1, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=15)
        
        tk.Button(btns, text="QUIT", font=("Helvetica", 18, "bold"),
                 bg="#95a5a6", fg="white", command=self.quit_app, width=6, height=1).pack(side=tk.RIGHT, padx=10, pady=15)
        
        self.status = tk.Label(btns, text="Connecting...", font=("Helvetica", 12), bg="#2c3e50", fg="#f39c12")
        self.status.pack(side=tk.RIGHT, padx=10)
        
        # Data display
        main = tk.Frame(self.root, bg="black")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left = tk.Frame(main, bg="black")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.speed = tk.Label(left, text="--", font=("Helvetica", 70, "bold"), bg="black", fg="white")
        self.speed.pack()
        tk.Label(left, text="km/h", font=("Helvetica", 16), bg="black", fg="gray").pack()
        
        self.rpm = tk.Label(left, text="RPM: --", font=("Helvetica", 20), bg="black", fg="white")
        self.rpm.pack(pady=10)
        self.throttle = tk.Label(left, text="Throttle: --", font=("Helvetica", 20), bg="black", fg="white")
        self.throttle.pack()
        
        right = tk.Frame(main, bg="#34495e", width=250)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        right.pack_propagate(False)
        
        self.trip_lbl = tk.Label(right, text="READY", font=("Helvetica", 14, "bold"), bg="#34495e", fg="#f39c12")
        self.trip_lbl.pack(pady=10)
        
        self.score_lbl = tk.Label(right, text="--", font=("Helvetica", 60, "bold"), bg="#34495e", fg="#2ecc71")
        self.score_lbl.pack(pady=10)
        self.grade = tk.Label(right, text="Grade: --", font=("Helvetica", 16), bg="#34495e", fg="white")
        self.grade.pack()
        self.events = tk.Label(right, text="Events: 0", font=("Helvetica", 13), bg="#34495e", fg="gray")
        self.events.pack(pady=10)
    
    def connection_monitor(self):
        """Continuously monitor and attempt OBD connection"""
        while self.running:
            if not self.connected:
                self.connection_attempts += 1
                status_msg = f"Connecting... (attempt {self.connection_attempts})"
                self.status.config(text=status_msg, fg="#f39c12")
                
                try:
                    # Create new OBD reader
                    if self.obd is None:
                        self.obd = OBDReader(
                            port=self.config.get("obd.port"),
                            baudrate=self.config.get("obd.baudrate")
                        )
                    
                    # Try to connect
                    if self.obd.connect(timeout=5):
                        self.connected = True
                        self.obd.start_async_reading(update_rate=0.1)
                        self.status.config(text="Connected ●", fg="#2ecc71")
                        self.start_btn.config(state=tk.NORMAL)
                        print(f"OBD connected after {self.connection_attempts} attempts")
                    else:
                        # Connection failed, wait before retry
                        time.sleep(3)
                except Exception as e:
                    print(f"Connection error: {e}")
                    time.sleep(3)
            else:
                # Already connected, just check status
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
                
                self.speed.config(text=f"{spd:.0f}")
                self.rpm.config(text=f"RPM: {rpm:.0f}")
                self.throttle.config(text=f"Throttle: {thr:.0f}%")
                
                if self.trip_active and self.last_data:
                    score, evt = self.scorer.update(speed_kph=spd, accel=self.last_data.get("accel_calculated", 0))
                    grade = self.scorer.get_grade()
                    self.score_lbl.config(text=f"{score:.0f}")
                    self.grade.config(text=f"Grade: {grade}")
                    self.score_lbl.config(fg="#2ecc71" if grade in ["A","B"] else "#f39c12" if grade=="C" else "#e74c3c")
                    self.events.config(text=f"Events: {self.scorer.harsh_brake_count + self.scorer.aggressive_accel_count}")
                    self.logger.log_data({**self.last_data, "score": score, "event_type": evt or ""})
            except Exception as e:
                print(f"Update error: {e}")
        
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
