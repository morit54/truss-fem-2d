import numpy as np
from math import sin, cos, tan
from .node import Node
from functools import cached_property

class TrussElement2D:
    def __init__(self,
                 number: int,
                 start_node: Node,
                 end_node: Node,
                 E=210000000.0,
                 A=0.02
                 ):
        """
        Args:
            number: number of the element (count)
            start_node: first node of the element
            end_node: second node of the element
            E: modulus of elasticity in [kN/m2]
            A: cross section area in [m2]
        """
        self.number = number
        self.start_node = start_node
        self.end_node = end_node
        self.E = E
        self.A = A

    @cached_property
    def length(self) -> float:
        """returns the length of the element in [m]"""
        delta_y = self.end_node.y - self.start_node.y
        delta_x = self.end_node.x - self.start_node.x
        length = (delta_y**2 + delta_x**2)**0.5
        return length

    @cached_property
    def alpha(self) -> float:
        """returns the angle of the element to the x-axis in [rad]"""
        delta_y = self.end_node.y - self.start_node.y
        delta_x = self.end_node.x - self.start_node.x
        alpha = tan(delta_y/delta_x)
        return alpha

    @cached_property
    def element_stiffness_matrix(self) -> np.ndarray:
        """returns the element stiffness matrix in the global coordinate system"""
        factor = self.E * self.A / self.length
        c = cos(self.length)
        s = sin(self.length)

        # column 1
        k11 = factor * c**2
        k21 = factor * s * c
        k31 = -k11
        k41 = -k21

        # column 2
        k12 = -k21
        k22 = factor * s**2
        k32 = -k21
        k42 = -k22

        # column 3
        k13 = -k11
        k23 = -k21
        k33 = k11
        k43 = k21

        # column 4
        k14 = -k21
        k24 = -k22
        k34 = k21
        k44 = k22


        matrix = np.array([
            [k11, k12, k13, k14],
            [k21, k22, k23, k24],
            [k31, k32, k33, k34],
            [k41, k42, k43, k44]
        ])
        return matrix



