#!/usr/bin/env python3
"""
Phase 1 GUI Monitor - Touchscreen Interface
Optimized for 800x480 display
"""

import sys
import os
import time
import pygame
from datetime import datetime

sys.path.insert(0, '/home/rays/carmonitor')

from phase1.obd_reader import OBDReader
from common.config import Config
from common.logger import TripLogger
from common.scoring import DriverScorer


class Phase1GUI:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Screen setup
        self.width = 800
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('BMW X5 Driver Monitor')
        pygame.mouse.set_visible(True)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (220, 50, 50)
        self.GREEN = (50, 200, 50)
        self.BLUE = (50, 150, 220)
        self.YELLOW = (255, 200, 0)
        self.ORANGE = (255, 140, 0)
        self.GRAY = (100, 100, 100)
        self.LIGHT_GRAY = (200, 200, 200)
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 28)
        
        # Load config
        self.config = Config('/home/rays/carmonitor/config/phase1_config.yaml')
        
        # Initialize components
        self.obd = OBDReader(
            port=self.config.get('obd.port'),
            baudrate=self.config.get('obd.baudrate')
        )
        self.logger = TripLogger(log_dir=self.config.get('logging.directory'))
        
        scorer_config = {
            "harsh_brake_threshold": self.config.get("scoring.harsh_brake_threshold"),
            "aggressive_accel_threshold": self.config.get("scoring.aggressive_accel_threshold"),
            "speeding_threshold": self.config.get("scoring.speeding_threshold")
        }
        self.scorer = DriverScorer(config=scorer_config)
        
        # State
        self.running = True
        self.trip_active = False
        self.connected = False
        self.last_data = {}
        
        # Buttons
        self.buttons = self._create_buttons()
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        
    def _create_buttons(self):
        button_height = 60
        button_width = 180
        y_pos = self.height - button_height - 20
        spacing = 20
        
        return {
            'start': pygame.Rect(20, y_pos, button_width, button_height),
            'stop': pygame.Rect(20 + button_width + spacing, y_pos, button_width, button_height),
            'quit': pygame.Rect(self.width - button_width - 20, y_pos, button_width, button_height)
        }
    
    def connect_obd(self):
        """Connect to OBD-II adapter"""
        if self.obd.connect():
            self.connected = True
            self.obd.start_async_reading(update_rate=0.1)
            return True
        return False
    
    def start_trip(self):
        """Start a new trip"""
        if not self.trip_active and self.connected:
            trip_name = datetime.now().strftime('trip_%Y%m%d_%H%M%S')
            self.logger.start_trip(trip_name)
            self.scorer.reset()
            self.trip_active = True
    
    def stop_trip(self):
        """Stop current trip"""
        if self.trip_active:
            self.logger.end_trip()
            self.trip_active = False
    
    def draw_button(self, name, rect, text, enabled=True):
        """Draw a touchscreen button"""
        color = self.GREEN if name == 'start' else self.RED if name == 'stop' else self.BLUE
        if not enabled:
            color = self.GRAY
        
        # Button background
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, rect, 3, border_radius=10)
        
        # Button text
        text_surface = self.font_small.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_status_bar(self):
        """Draw top status bar"""
        # Background
        pygame.draw.rect(self.screen, self.BLUE, (0, 0, self.width, 60))
        
        # Title
        title = self.font_medium.render('BMW X5 Driver Monitor', True, self.WHITE)
        self.screen.blit(title, (20, 12))
        
        # Connection status
        status_text = 'CONNECTED' if self.connected else 'DISCONNECTED'
        status_color = self.GREEN if self.connected else self.RED
        status = self.font_tiny.render(status_text, True, status_color)
        self.screen.blit(status, (self.width - 180, 20))
    
    def draw_trip_status(self):
        """Draw trip status section"""
        y_pos = 80
        
        if self.trip_active:
            status_text = 'TRIP ACTIVE'
            color = self.GREEN
        else:
            status_text = 'NO ACTIVE TRIP'
            color = self.ORANGE
        
        status = self.font_medium.render(status_text, True, color)
        status_rect = status.get_rect(center=(self.width // 2, y_pos))
        self.screen.blit(status, status_rect)
    
    def draw_vehicle_data(self):
        """Draw main vehicle data display"""
        y_start = 140
        
        # Speed (large and prominent)
        speed = self.last_data.get('speed_kph', 0)
        speed_text = self.font_large.render(f"{speed:.0f}", True, self.WHITE)
        speed_label = self.font_small.render('km/h', True, self.LIGHT_GRAY)
        
        self.screen.blit(speed_text, (50, y_start))
        self.screen.blit(speed_label, (50, y_start + 80))
        
        # RPM
        rpm = self.last_data.get('rpm', 0)
        rpm_text = self.font_medium.render(f"{rpm:.0f}", True, self.WHITE)
        rpm_label = self.font_tiny.render('RPM', True, self.LIGHT_GRAY)
        
        self.screen.blit(rpm_text, (250, y_start + 10))
        self.screen.blit(rpm_label, (250, y_start + 65))
        
        # Throttle
        throttle = self.last_data.get('throttle_pct', 0)
        throttle_text = self.font_medium.render(f"{throttle:.0f}%", True, self.WHITE)
        throttle_label = self.font_tiny.render('Throttle', True, self.LIGHT_GRAY)
        
        self.screen.blit(throttle_text, (250, y_start + 90))
        self.screen.blit(throttle_label, (250, y_start + 145))
    
    def draw_score_panel(self):
        """Draw driver score panel"""
        x_pos = 480
        y_pos = 140
        
        # Score box
        box_rect = pygame.Rect(x_pos, y_pos, 280, 180)
        pygame.draw.rect(self.screen, self.GRAY, box_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.WHITE, box_rect, 3, border_radius=15)
        
        if self.trip_active:
            score = self.scorer.get_score()
            grade = self.scorer.get_grade()
            
            # Determine color based on grade
            if grade in ['A', 'B']:
                score_color = self.GREEN
            elif grade == 'C':
                score_color = self.YELLOW
            else:
                score_color = self.RED
            
            # Score
            score_text = self.font_large.render(f"{score:.0f}", True, score_color)
            score_rect = score_text.get_rect(center=(x_pos + 140, y_pos + 60))
            self.screen.blit(score_text, score_rect)
            
            # Grade
            grade_text = self.font_medium.render(f"Grade: {grade}", True, self.WHITE)
            grade_rect = grade_text.get_rect(center=(x_pos + 140, y_pos + 130))
            self.screen.blit(grade_text, grade_rect)
        else:
            # Not tracking
            no_trip = self.font_small.render('Start trip', True, self.LIGHT_GRAY)
            no_trip_rect = no_trip.get_rect(center=(x_pos + 140, y_pos + 50))
            self.screen.blit(no_trip, no_trip_rect)
            
            no_trip2 = self.font_small.render('to track score', True, self.LIGHT_GRAY)
            no_trip2_rect = no_trip2.get_rect(center=(x_pos + 140, y_pos + 90))
            self.screen.blit(no_trip2, no_trip2_rect)
    
    def draw_events(self):
        """Draw event counters"""
        y_pos = 340
        
        harsh_brakes = self.scorer.harsh_brake_count
        aggressive_accels = self.scorer.aggressive_accel_count
        
        # Harsh brakes
        harsh_text = self.font_tiny.render(f"Harsh Brakes: {harsh_brakes}", True, self.RED)
        self.screen.blit(harsh_text, (50, y_pos))
        
        # Aggressive acceleration
        accel_text = self.font_tiny.render(f"Aggressive Accel: {aggressive_accels}", True, self.ORANGE)
        self.screen.blit(accel_text, (300, y_pos))
    
    def handle_click(self, pos):
        """Handle touch/click events"""
        if self.buttons['start'].collidepoint(pos):
            self.start_trip()
        elif self.buttons['stop'].collidepoint(pos):
            self.stop_trip()
        elif self.buttons['quit'].collidepoint(pos):
            self.running = False
    
    def update(self):
        """Update data from OBD"""
        if self.connected:
            self.last_data = self.obd.get_latest_data()
            
            if self.trip_active and self.last_data:
                # Update scorer
                score, event_type = self.scorer.update(
                    speed_kph=self.last_data.get('speed_kph', 0),
                    accel=self.last_data.get('accel_calculated', 0)
                )
                
                # Log data
                log_data = {
                    **self.last_data,
                    'score': score,
                    'event_type': event_type if event_type else ''
                }
                self.logger.log_data(log_data)
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw components
        self.draw_status_bar()
        self.draw_trip_status()
        self.draw_vehicle_data()
        self.draw_score_panel()
        self.draw_events()
        
        # Draw buttons
        self.draw_button('start', self.buttons['start'], 'START TRIP', 
                        enabled=(self.connected and not self.trip_active))
        self.draw_button('stop', self.buttons['stop'], 'STOP TRIP', 
                        enabled=self.trip_active)
        self.draw_button('quit', self.buttons['quit'], 'QUIT', enabled=True)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        print("Starting main loop...")
        """Main loop"""
        # Try to connect
        print("Connecting to OBD-II adapter...")
        if not self.connect_obd():
            print("Failed to connect to OBD-II adapter")
            # Continue anyway to show GUI
        
        # Main loop
        while self.running:
            print(f"Loop iteration, running={self.running}")
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_s:
                        self.start_trip()
                    elif event.key == pygame.K_x:
                        self.stop_trip()
            
            # Update data
            self.update()
            
            # Draw
            self.draw()
            
            # Control frame rate
            self.clock.tick(10)  # 10 FPS
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.trip_active:
            self.stop_trip()
        if self.connected:
            self.obd.disconnect()
        pygame.quit()


def main():
    gui = Phase1GUI()
    gui.run()


if __name__ == '__main__':
    main()
