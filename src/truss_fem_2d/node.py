from dataclasses import dataclass

@dataclass
class Node:
    """
    Args:
        x: x-coordinate of the node
        y: y-coordinate of the node
        Fx: horizontal force in [kN]
        Fy: vertical force in [kN]
    """
    x: float
    y: float
    Fx=0.0
    Fy=0.0






