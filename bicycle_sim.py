from dataclasses import dataclass

import numpy as np


@dataclass
class BicycleConfig:
    """Dataclass for storing bicycle model parameters."""
    # Physical dimensions
    body_length: float = 1.5  # Distance between front and rear wheels (m)
    wheel_radius: float = 0.25  # Wheel radius for visualization (m)
    
    # Performance limits
    max_acceleration: float = 2.0   # (m/s^2)
    max_speed: float = 10.0  # (m/s)
    max_steering: float = np.pi / 4 # (radians)


class BicycleSimulation:
    """Class representing a bicycle simulation using kinematic equations.
    
    State variables: [x, y, theta, v, delta]
    x, y: Position of the rear wheel.
    theta: Orientation angle (radians).
    v: Velocity (m/s).
    delta: Steering angle (radians).

    Control inputs: acceleration and steering rate.

    The bicycle can't move backwards and be steered beyond max steering angle
    (both clockwise and counter clockwise). It also can't move faster than the
    max speed, specified in Bicycle config.
    """

    def __init__(self, config=None, dt=0.1):
        """Initializes the simulation.

        Args:
            config: An optional BicycleConfig instance.
            dt: Time step for the simulation (in seconds).
        """
        self.config = config or BicycleConfig()
        self.dt = dt
        self.state = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

        # History for plotting trail.
        self.history = []

    def bicycle_kinematics(self, state, accel, steering_rate):
        """Computes the next state using the bicycle kinematic model.

        Args:
            state: Current state [x, y, theta, v, delta].
            accel: Acceleration input.
            steering_rate: Rate of change of the steering angle.

        Returns:
            The updated state as a NumPy array.
        """
        x, y, theta, v, delta = state

        # Update steering angle.
        delta_new = np.clip(
            delta + steering_rate * self.dt,
            -self.config.max_steering,
            self.config.max_steering
        )

        # Update velocity.
        v_new = np.clip(v + accel * self.dt, 0, self.config.max_speed)

        # Compute slip angle.
        beta = np.arctan(0.5 * np.tan(delta))

        # Update position and orientation.
        x_new = x + v_new * np.cos(theta + beta) * self.dt
        y_new = y + v_new * np.sin(theta + beta) * self.dt
        theta_new = theta + (v_new / self.config.body_length) * np.sin(beta) * self.dt

        # Normalize theta to [-pi, pi].
        theta_new = np.arctan2(np.sin(theta_new), np.cos(theta_new))

        return np.array([x_new, y_new, theta_new, v_new, delta_new])
    
    def update(self, acceleration=0.0, steering_rate=0.0):
        """Update simulation one time step"""
        acceleration = np.clip(acceleration,
                               -self.config.max_acceleration,
                               self.config.max_acceleration)
        self.state = self.bicycle_kinematics(self.state, acceleration, steering_rate)
        self.history.append(self.state[:2].copy())  # Store position
        
        # Limit history length
        if len(self.history) > 500:
            self.history.pop(0)
    
    def get_bicycle_shape(self):
        """Get bicycle shape as lines for visualization"""
        x, y, theta, _, delta = self.state
        
        # Bicycle dimensions
        length = self.config.body_length
        wheel_radius = self.config.wheel_radius
        
        # Rear wheel center (reference point)
        rear_x, rear_y = x, y
        
        # Front wheel center
        front_x = rear_x + length * np.cos(theta)
        front_y = rear_y + length * np.sin(theta)
        
        # Bicycle body (single line from rear to front)
        body_line = np.array([[rear_x, rear_y], [front_x, front_y]])
        
        # Rear wheel (line aligned with body direction)
        rear_wheel_x = wheel_radius * np.cos(theta)
        rear_wheel_y = wheel_radius * np.sin(theta)
        rear_wheel_line = np.array([
            [rear_x - rear_wheel_x, rear_y - rear_wheel_y],
            [rear_x + rear_wheel_x, rear_y + rear_wheel_y]
        ])
        
        # Front wheel (line aligned with body + steering angle)
        front_theta = theta + delta
        front_wheel_x = wheel_radius * np.cos(front_theta)
        front_wheel_y = wheel_radius * np.sin(front_theta)
        front_wheel_line = np.array([
            [front_x - front_wheel_x, front_y - front_wheel_y],
            [front_x + front_wheel_x, front_y + front_wheel_y]
        ])
        
        return body_line, rear_wheel_line, front_wheel_line
