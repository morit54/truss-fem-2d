from dataclasses import dataclass
from enum import Enum
from typing import Literal

class DegreeOfFreedom(Enum):
    """
    # DegreeOfFreedom
    ## purpose
    - choose, if a Node is fixed or movable

    ## why not Boolean?
    - readability
    - string values can be used for a dropdown menu -> [dof.value for dof in DegreeOfFreedom]

    Args:
        FIXED: the node <u>is not movable</u> for the individual Node and it's x or y direction
        MOVABLE: the node <u>is movable</u> for the individual Node and it's x or y direction
    """
    FIXED = "fixed"
    MOVABLE = "movable"

@dataclass
class Node:
    """
    # Node
    ## purpose
    - store information about the Node for later use
    - used to define the specific static system

    Args:
        number: the number of the node (count)
        x: x-coordinate of the node
        y: y-coordinate of the node
        x_dof: the node can be movable or fixed in x-axis
        y_dof: the node can be movable or fixed in y-axis
        Fx: horizontal force in [kN]
        Fy: vertical force in [kN]
    """
    number: int
    x: float
    y: float
    x_dof: DegreeOfFreedom = DegreeOfFreedom.MOVABLE
    y_dof: DegreeOfFreedom = DegreeOfFreedom.MOVABLE
    Fx: float = 0.0
    Fy: float = 0.0




