from functools import cached_property
import numpy as np
from .static_system import StaticSystem
from .node import DegreeOfFreedom

class LinearTrussSolver:
    def __init__(self, static_system: StaticSystem):
        self.static_system = static_system

    @cached_property
    def dof(self) -> int:
        """
        # degrees of freedom 
        - returns the degrees of freedom
        - each node has got two degrees of freedom
        - equal to the size of the system stiffness matrix 
        """
        dof = len(self.static_system.list_of_nodes) * 2
        return dof

    @cached_property
    def delete_list(self) -> list:
        """
        # delete list
        list of indices of the rows and columns that need to be deleted
        """
        indices = []
        for node in self.static_system.list_of_nodes:
            if node.x_dof == DegreeOfFreedom.FIXED:
                indices.append(node.number*2-2)
            if node.y_dof == DegreeOfFreedom.FIXED:
                indices.append(node.number*2-1)
        return indices
    
    @cached_property
    def system_stiffness_matrix(self) -> np.ndarray:
        """
        Assembles the system stiffness matrix and returns it as
        a NumPy array.
        """
        all_elements = self.static_system.list_of_elements
        matrix = np.zeros((self.dof, self.dof))
        for element in all_elements:
            node1 = element.start_node.number
            node2 = element.end_node.number
            index = (
                node1*2-2,
                node1*2-1,
                node2*2-2,
                node2*2-1
            )
            for r, element_row in enumerate(element.element_stiffness_matrix): # r -> row index
                for c, element_value in enumerate(element_row): # c -> column index
                    row = index[r]
                    col = index[c]
                    matrix[row][col] += element_value
        return matrix

    @cached_property
    def load_vector(self) -> np.ndarray:
        """creates the load vector"""
        vector = [0]*self.dof
        for node in self.static_system.list_of_nodes:
            Fx_index = node.number*2-2
            Fy_index = node.number*2-1
            vector[Fx_index] += node.Fx
            vector[Fy_index] += node.Fy
        return np.array(vector)

    @cached_property
    def system_stiffness_matrix_reduced(self) -> np.ndarray:
        """
        # Reduced system stiffness matrix
        - needed for solving the linear system of equations
        - removes the degrees of freedom (rows and columns), that are fixed
        """
        matrix = np.delete(
            np.delete(
                self.system_stiffness_matrix, self.delete_list, axis=0),
                    self.delete_list, axis=1)
        return matrix

    @cached_property
    def load_vector_reduced(self) -> np.ndarray:
        """
        # Reduced load vector
        - needed for solving the linear system of equations
        - removes the degrees of freedom (rows and columns), that are fixed
        """
        vector_reduced = np.delete(self.load_vector, self.delete_list, axis=0)
        return vector_reduced

    @cached_property
    def displacements_reduced(self) -> np.ndarray:
        """
        # reduced displacements in [m]
        - solves the linear system of equations
        - returns the reduced displacements as a list
        - reduced -> without the zeros of the fixed dof's
        """
        displacements = np.linalg.solve(self.system_stiffness_matrix_reduced, self.load_vector_reduced)
        return displacements

    @cached_property
    def displacements(self) -> np.ndarray:
        """
        # displacements in [m]
        """
        # create the list of all displacements
        displacements = [None]*self.dof

        # fill the zeros
        for index in self.delete_list:
            displacements[index] = 0

        # fill in the values from the displacements_reduced list
        k = 0
        for i, value in enumerate(displacements):
            if value == None:
                displacements[i] = self.displacements_reduced[k]
                k += 1
            elif value == 0:
                pass
        return np.array(displacements)




