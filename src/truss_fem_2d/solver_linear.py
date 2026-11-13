from functools import cached_property
import numpy as np
from .static_system import StaticSystem
from .node import DegreeOfFreedom
from .element import TrussElement2D
from .utils import num_round

def _get_normal_force(
        element: TrussElement2D,
        disp_vector: np.ndarray
        ):
    """
    # get normal force
    - checks if the element either got stretched- or compressed
      - stretched -> positive normal force (tension)
      - compressed -> negative normal force (compression)
    """
    force_vector = element.element_stiffness_matrix @ disp_vector
    # get initial coordinates
    x1, y1, x2, y2 = (element.start_node.x, element.start_node.y, element.end_node.x, element.end_node.y)
    
    # get displacements
    x1_disp, y1_disp, x2_disp, y2_disp = disp_vector
    
    # get new coordinates
    x1_new = x1 + x1_disp
    y1_new = y1 + y1_disp
    x2_new = x2 + x2_disp
    y2_new = y2 + y2_disp
    
    # calculate new length
    l_new = ((x2_new-x1_new)**2 + (y2_new-y1_new)**2)**0.5
    
    # decide if the normal force is positive or negative
    if l_new < element.length:
        Fx = force_vector[0]
        Fy = force_vector[1]
        N = - (Fx**2 + Fy**2)**0.5
    else:
        Fx = force_vector[0]
        Fy = force_vector[1]
        N = (Fx**2 + Fy**2)**0.5
    return N



class LinearTrussSolver:
    """
    # Linear Truss Solver
    ## description
    This solver uses the finite element method (2D) to assemble- and calculate the linear system of equations.
    """
    def __init__(self, static_system: StaticSystem):
        self.static_system = static_system

    @cached_property
    def dof(self) -> int:
        """
        # degrees of freedom 
        - returns the degrees of freedom
        - each node has got two degrees of freedom
        - dof is equal to the size of the system stiffness matrix 
        """
        dof = len(self.static_system.list_of_nodes) * 2
        return dof

    @cached_property
    def delete_list(self) -> list:
        """
        # delete list
        - list of indices of the rows and columns that need to be deleted from the system stiffness matrix
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
        # system stiffness matrix
        - Assembles the system stiffness matrix and returns it as
         a NumPy array.
        """
        # list of all elements
        all_elements = self.static_system.list_of_elements

        # create square matrix filled with zeros
        matrix = np.zeros((self.dof, self.dof))

        # do this for each element
        for element in all_elements:
            node1 = element.start_node.number
            node2 = element.end_node.number
            index = (
                node1*2-2,
                node1*2-1,
                node2*2-2,
                node2*2-1
            )
            # do this for each row of the current element stiffness matrix
            for r, element_row in enumerate(element.element_stiffness_matrix): # r -> row index
                # do this for each value (column) of a row of the element stiffness matrix
                for c, matrix_value in enumerate(element_row): # c -> column index
                    row = index[r]
                    col = index[c]
                    matrix[row][col] += matrix_value
        return matrix

    @cached_property
    def load_vector(self) -> np.ndarray:
        """
        # load vector
        - creates the load vector and returns it as a NumPy array
        """
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
        - returns the reduced displacements as a NumPy array
        - reduced -> without the zeros of the fixed dof's
        """
        displacements = np.linalg.solve(self.system_stiffness_matrix_reduced, self.load_vector_reduced)
        return displacements

    @cached_property
    def displacements(self) -> np.ndarray:
        """
        # displacements in [m]
        When the system of equations is solved, the results do not contain the zeros
        from the deleted dof's. This method returns the complete displacements as a NumPy array
        by just adding the zeros of the deleted dof's at the correct positions.
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

    @cached_property
    def normal_forces(self) -> list[float]:
        """
        # normal forces
        - returns a regular Python list of all normal forces
        """
        normal_forces = []
        for element in self.static_system.list_of_elements:
            node_no1 = element.start_node.number
            node_no2 = element.end_node.number
            # create displacement vector for this element
            disp = np.array([
                self.displacements[node_no1*2-2],
                self.displacements[node_no1*2-1],
                self.displacements[node_no2*2-2],
                self.displacements[node_no2*2-1]
            ])
            # print(disp)
            # create force vecor for this element
            n_force = _get_normal_force(
                element=        element,
                disp_vector=    disp
            )
            normal_forces.append(n_force)
        return [float(val) for val in normal_forces]

    @cached_property
    def support_forces(self):
        """
        # support forces
        - calculates the support forces of the fixed nodes.
        """
        # multiply the deleted rows with the displacements
        forces = []
        for i in self.delete_list:
            support_force = self.system_stiffness_matrix[i] @ self.displacements
            forces.append(float(support_force))
        return forces

    def print_results(self) -> None:
        """
        # print results
        - prints support reactions of the fixed nodes
        - prints normal forces in the console
        """
        print("--- SUPPORT FORCES ---")
        Fxy = ["Fx", "Fy"]
        for i, support_force in enumerate(self.support_forces):
            dof_index = self.delete_list[i]
            node_no = int(dof_index/2) + 1
            text = f"{Fxy[dof_index % 2]}{node_no} = {num_round(support_force, 2)} [kN]"
            print(text)

        print("\n--- NORMAL FORCES ---")
        # print normal forces
        for i, N in enumerate(self.normal_forces):
            print(f"N{i+1} = {num_round(N, 2)} [kN]")
        return None


        



