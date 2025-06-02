from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass
class CircleTarget:
    """Represents a circular target for the bicycle to reach."""
    center: Tuple[float, float]
    radius: float
    
    @property
    def x(self) -> float:
        """X coordinate of the target center."""
        return self.center[0]
    
    @property
    def y(self) -> float:
        """Y coordinate of the target center."""
        return self.center[1]
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is inside the target circle."""
        distance = np.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.radius
    
    def distance_to_point(self, x: float, y: float) -> float:
        """Calculate distance from a point to the target center."""
        return np.sqrt((x - self.x)**2 + (y - self.y)**2)
    
    def distance_to_boundary(self, x: float, y: float) -> float:
        """Calculate distance from a point to the target boundary.
        
        Returns:
            Positive if outside, negative if inside the circle.
        """
        return self.distance_to_point(x, y) - self.radius
    
    @classmethod
    def from_string(cls, input_str: str) -> 'CircleTarget':
        """Create a CircleTarget from a string like 'x,y,radius'."""
        parts = input_str.strip().split(',')
        if len(parts) != 3:
            raise ValueError("Input must be in format 'x,y,radius'")
        x, y, radius = map(float, parts)
        return cls(center=(x, y), radius=radius)
    
    def __str__(self) -> str:
        return f"CircleTarget(center=({self.x}, {self.y}), radius={self.radius})"
