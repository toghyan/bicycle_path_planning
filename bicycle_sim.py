import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass


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

# Create simulation
sim = BicycleSimulation()

# Set up the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Main simulation plot
ax1.set_xlim(-15, 15)
ax1.set_ylim(-15, 15)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.set_title('2D Bicycle Simulation')
ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')

# Initialize plot elements
trail_line, = ax1.plot([], [], 'b-', alpha=0.5, linewidth=1, label='Trail')
body_line, = ax1.plot([], [], 'k-', linewidth=2, label='Body')
rear_wheel_line, = ax1.plot([], [], 'r-', linewidth=3, label='Rear Wheel')
front_wheel_line, = ax1.plot([], [], 'g-', linewidth=3, label='Front Wheel')
ax1.legend()

# State plot
ax2.set_xlim(0, 100)
ax2.set_ylim(-5, 15)
ax2.grid(True, alpha=0.3)
ax2.set_title('Bicycle State')
ax2.set_xlabel('Time Steps')
ax2.set_ylabel('Value')

# State history
time_history = []
speed_history = []
steering_history = []

speed_line, = ax2.plot([], [], 'b-', label='Speed (m/s)')
steering_line, = ax2.plot([], [], 'r-', label='Steering Angle (rad)')
ax2.legend()

# Control variables
time_step = 0

def animate(frame):
    global time_step
    
    # Simple control logic - create interesting motion
    t = time_step * sim.dt
    acceleration = 0.0
    steering_rate = 0.0
    
    # Acceleration pattern
    if t < 5:
        acceleration = 2.0  # Accelerate
    elif t < 10:
        acceleration = 0.0  # Coast
    elif t < 15:
        acceleration = -1.0  # Brake
    else:
        acceleration = 0.5  # Gentle acceleration
    
    # Steering pattern
    if 3 < t < 8:
        steering_rate = 0.5  # Turn right
    elif 10 < t < 15:
        steering_rate = -0.8  # Turn left
    elif 20 < t < 25:
        steering_rate = 0.3  # Gentle right turn
    else:
        steering_rate = -0.1 * sim.state[4]  # Return to center
    
    # Update simulation
    sim.update(acceleration, steering_rate)
    time_step += 1
    
    # Get bicycle shape.
    body, rear_wheel, front_wheel = sim.get_bicycle_shape()
    
    # Update trail
    if len(sim.history) > 1:
        trail_x = [pos[0] for pos in sim.history]
        trail_y = [pos[1] for pos in sim.history]
        trail_line.set_data(trail_x, trail_y)
    
    # Update bicycle
    body_line.set_data(body[:, 0], body[:, 1])
    rear_wheel_line.set_data(rear_wheel[:, 0], rear_wheel[:, 1])
    front_wheel_line.set_data(front_wheel[:, 0], front_wheel[:, 1])
    
    # Update state plots
    time_history.append(time_step)
    speed_history.append(sim.state[3])
    steering_history.append(sim.state[4])
    
    # Keep only recent history for state plots
    if len(time_history) > 200:
        time_history.pop(0)
        speed_history.pop(0)
        steering_history.pop(0)
        ax2.set_xlim(time_step - 200, time_step)
    
    speed_line.set_data(time_history, speed_history)
    steering_line.set_data(time_history, steering_history)
    
    # Update bicycle position in view
    x, y = sim.state[0], sim.state[1]
    ax1.set_xlim(x - 10, x + 10)
    ax1.set_ylim(y - 10, y + 10)
    
    return trail_line, body_line, rear_wheel_line, front_wheel_line, speed_line, steering_line

# Create and run animation
anim = animation.FuncAnimation(fig, animate, interval=50, blit=True, cache_frame_data=False)

# Add text with instructions
fig.suptitle('2D Bicycle Simulation - Watch the bicycle navigate with automatic steering and acceleration patterns')

plt.tight_layout()
plt.show()

# Optional: Save as gif (uncomment to save)
# anim.save('bicycle_simulation.gif', writer='pillow', fps=20)