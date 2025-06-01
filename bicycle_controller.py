import numpy as np
from abc import ABC, abstractmethod


class BicycleController(ABC):
    """Abstract base class for bicycle controllers."""
    
    @abstractmethod
    def compute_control(self, state, target, dt):
        """
        Compute control inputs for the bicycle.
        
        Args:
            state: Current state [x, y, theta, v, delta]
            target: Target information (e.g., position, circle)
            dt: Time step
            
        Returns:
            tuple: (acceleration, steering_rate)
        """
        pass


class SimpleTargetController(BicycleController):
    """Simple controller that drives towards a target circle."""
    
    def __init__(self, max_acceleration=2.0, max_steering_rate=1.0):
        self.max_acceleration = max_acceleration
        self.max_steering_rate = max_steering_rate
        
    def compute_control(self, state, target):
        """
        Simple control law to reach target circle.
        
        Args:
            state: [x, y, theta, v, delta]
            target: dict with 'center' (x, y) and 'radius'
        """
        x, y, theta, v, _ = state
        target_x, target_y = target['center']
        target_radius = target['radius']
        
        # Compute distance and angle to target center
        dx = target_x - x
        dy = target_y - y
        distance = np.sqrt(dx**2 + dy**2)
        
        # Angle to target
        desired_theta = np.arctan2(dy, dx)
        
        # Normalize angle difference
        theta_error = desired_theta - theta
        theta_error = np.arctan2(np.sin(theta_error), np.cos(theta_error))
        
        # Simple control logic
        # Steering: proportional to angle error
        steering_rate = np.clip(2.0 * theta_error, -self.max_steering_rate, self.max_steering_rate)
        
        # Acceleration: slow down when close to target, speed up when far
        if distance <= target_radius:
            # Inside target circle - stop
            acceleration = -v * 2.0  # Brake proportional to current speed
        elif distance < target_radius * 3:
            # Close to target - slow down
            acceleration = (distance - target_radius) * 0.5 - v * 0.5
        else:
            # Far from target - speed up
            acceleration = min(2.0, distance * 0.1)
            
        # Reduce speed when turning sharply
        if abs(theta_error) > np.pi/4:
            acceleration = min(acceleration, 0.5)
            
        acceleration = np.clip(acceleration, -self.max_acceleration, self.max_acceleration)
        
        return acceleration, steering_rate


class ManualController(BicycleController):
    """Controller for manual input (keyboard or predefined sequence)."""
    
    def __init__(self):
        self.acceleration = 0.0
        self.steering_rate = 0.0
        
    def set_controls(self, acceleration, steering_rate):
        """Set control inputs manually."""
        self.acceleration = acceleration
        self.steering_rate = steering_rate
        
    def compute_control(self, state, target, dt):
        """Return the manually set controls."""
        return self.acceleration, self.steering_rate