import matplotlib.patches as patches
from target import CircleTarget


class BicycleAnimator:
    """Handles animation and visualization of bicycle simulation."""
    
    def __init__(self, sim, controller, target: CircleTarget, fig, ax1, ax2):
        self.sim = sim
        self.controller = controller
        self.target = target
        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2
        
        # Animation state
        self.time_step = 0
        self.simulation_complete = False
        
        # State history for plots
        self.time_history = []
        self.speed_history = []
        self.steering_history = []
        self.distance_history = []
        
        # Initialize plot elements
        self._setup_plots()
        
    def _setup_plots(self):
        """Initialize all plot elements."""
        # Add target circle
        self.target_circle = patches.Circle(
            self.target.center, self.target.radius, 
            fill=False, edgecolor='purple', linewidth=2, 
            linestyle='--', label='Target'
        )
        self.ax1.add_patch(self.target_circle)
        
        # Add filled circle to show target area
        self.target_fill = patches.Circle(
            self.target.center, self.target.radius, 
            fill=True, facecolor='purple', alpha=0.2
        )
        self.ax1.add_patch(self.target_fill)
        
        # Initialize bicycle plot elements
        self.trail_line, = self.ax1.plot([], [], 'b-', alpha=0.5, linewidth=1, label='Trail')
        self.body_line, = self.ax1.plot([], [], 'k-', linewidth=2, label='Body')
        self.rear_wheel_line, = self.ax1.plot([], [], 'r-', linewidth=3, label='Rear Wheel')
        self.front_wheel_line, = self.ax1.plot([], [], 'g-', linewidth=3, label='Front Wheel')
        
        # Add text to show distance to target
        self.distance_text = self.ax1.text(
            0.02, 0.98, '', transform=self.ax1.transAxes, 
            verticalalignment='top', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        self.ax1.legend()
        
        # State plot lines
        self.speed_line, = self.ax2.plot([], [], 'b-', label='Speed (m/s)')
        self.steering_line, = self.ax2.plot([], [], 'r-', label='Steering Angle (rad)')
        self.distance_line, = self.ax2.plot([], [], 'g-', label='Distance to Target (m)')
        self.ax2.legend()
        
        # Store all artists for blitting
        self.artists = [
            self.trail_line, self.body_line, self.rear_wheel_line, 
            self.front_wheel_line, self.speed_line, self.steering_line, 
            self.distance_line
        ]
        
    def animate(self, frame):
        """Animation function called each frame."""
        if self.simulation_complete:
            return self.artists
        
        # Get control inputs from controller
        acceleration, steering_rate = self.controller.compute_control(
            self.sim.state, self.target
        )
        
        # Update simulation
        self.sim.update(acceleration, steering_rate)
        self.time_step += 1
        
        # Calculate distance to target
        x, y = self.sim.state[0], self.sim.state[1]
        distance_to_target = self.target.distance_to_point(x, y)
        
        # Update distance text
        status = "Inside target!" if self.target.contains_point(x, y) else f"Distance: {distance_to_target:.2f}m"
        self.distance_text.set_text(status)
        
        # Check if we've reached the target and stayed there
        if self.target.contains_point(x, y) and self.sim.state[3] < 0.1:
            self.simulation_complete = True
            self.distance_text.set_text(f"Target reached! Final distance: {distance_to_target:.2f}m")
        
        # Update bicycle visualization
        self._update_bicycle()
        
        # Update state plots
        self._update_state_plots(distance_to_target)
        
        # Update view if needed
        self._update_view(x, y)
        
        return self.artists
    
    def _update_bicycle(self):
        """Update bicycle position and trail."""
        # Get bicycle shape
        body, rear_wheel, front_wheel = self.sim.get_bicycle_shape()
        
        # Update trail
        if len(self.sim.history) > 1:
            trail_x = [pos[0] for pos in self.sim.history]
            trail_y = [pos[1] for pos in self.sim.history]
            self.trail_line.set_data(trail_x, trail_y)
        
        # Update bicycle components
        self.body_line.set_data(body[:, 0], body[:, 1])
        self.rear_wheel_line.set_data(rear_wheel[:, 0], rear_wheel[:, 1])
        self.front_wheel_line.set_data(front_wheel[:, 0], front_wheel[:, 1])
        
    def _update_state_plots(self, distance_to_target):
        """Update the state history plots."""
        # Add new data
        self.time_history.append(self.time_step)
        self.speed_history.append(self.sim.state[3])
        self.steering_history.append(self.sim.state[4])
        self.distance_history.append(distance_to_target)
        
        # Keep only recent history
        max_history = 200
        if len(self.time_history) > max_history:
            self.time_history.pop(0)
            self.speed_history.pop(0)
            self.steering_history.pop(0)
            self.distance_history.pop(0)
            self.ax2.set_xlim(self.time_step - max_history, self.time_step)
        
        # Update plot lines
        self.speed_line.set_data(self.time_history, self.speed_history)
        self.steering_line.set_data(self.time_history, self.steering_history)
        self.distance_line.set_data(self.time_history, self.distance_history)
        
    def _update_view(self, x, y):
        """Update plot view if bicycle moves outside current bounds."""
        xlim = self.ax1.get_xlim()
        ylim = self.ax1.get_ylim()
        
        # Check if we need to expand the view
        margin = 5
        update_view = False
        new_xlim = list(xlim)
        new_ylim = list(ylim)
        
        if x - margin < xlim[0]:
            new_xlim[0] = x - margin
            update_view = True
        if x + margin > xlim[1]:
            new_xlim[1] = x + margin
            update_view = True
        if y - margin < ylim[0]:
            new_ylim[0] = y - margin
            update_view = True
        if y + margin > ylim[1]:
            new_ylim[1] = y + margin
            update_view = True
            
        if update_view:
            self.ax1.set_xlim(new_xlim)
            self.ax1.set_ylim(new_ylim)
