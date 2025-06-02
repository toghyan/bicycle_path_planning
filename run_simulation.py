import matplotlib.pyplot as plt
import matplotlib.animation as animation

from bicycle_animator import BicycleAnimator
from bicycle_sim import BicycleSimulation
from bicycle_controller import SimpleTargetController
from target import CircleTarget


def main():
    # Create simulation and controller
    sim = BicycleSimulation()
    controller = SimpleTargetController(max_acceleration=2.0, max_steering_rate=1.0, dt=0.1)
    
    # Define default target
    target = CircleTarget(center=(10.0, 8.0), radius=2.0)
    
    # Allow user to customize target
    try:
        print(f"Default target: {target}")
        user_input = input("Enter target as 'x,y,radius' or press Enter for default: ").strip()
        if user_input:
            target = CircleTarget.from_string(user_input)
            print(f"Target set to: {target}")
    except ValueError as e:
        print(f"Invalid input: {e}. Using default target.")

    # Set up the figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Configure main simulation plot
    view_margin = 5
    min_x = min(0, target.x - target.radius) - view_margin
    max_x = max(0, target.x + target.radius) + view_margin
    min_y = min(0, target.y - target.radius) - view_margin
    max_y = max(0, target.y + target.radius) + view_margin
    
    ax1.set_xlim(min_x, max_x)
    ax1.set_ylim(min_y, max_y)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('2D Bicycle Simulation')
    ax1.set_xlabel('X Position (m)')
    ax1.set_ylabel('Y Position (m)')

    # Configure state plot
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-5, 15)
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Bicycle State')
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Value')

    # Create animator
    animator = BicycleAnimator(sim, controller, target, fig, ax1, ax2)

    # Create and run animation
    anim = animation.FuncAnimation(
        fig, animator.animate, interval=50, blit=True, cache_frame_data=False
    )

    # Add title with controller info
    fig.suptitle(f'Bicycle Target Navigation - {target}')

    plt.tight_layout()
    plt.show()

    # Optional: Save as gif
    # anim.save('bicycle_navigation.gif', writer='pillow', fps=20)


if __name__ == '__main__':
    main()