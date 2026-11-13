from .node import Node, DegreeOfFreedom
from .element import TrussElement2D
import matplotlib.pyplot as plt
from .check_input import check_dof_input

class StaticSystem:
    """
    # StaticSystem
    ## description
    The static system is defined by adding the nodes and elements, by using the
    **.add_node()** and **.add_element()** methods.
    The nodes and the elements must be added in chronological order.

    ## purpose
    - Check if the system satisfies basic requirements.
    - Check if the static system is movable.

    ## example
    ### add the nodes to the system
    StaticSystem.add_node(x=0.00, y=0.00, x_dof=DegreeOfFreedom.FIXED, y_dof=DegreeOfFreedom.FIXED)  
    StaticSystem.add_node(x=0.90, y=0.00)  
    StaticSystem.add_node(x=0.70, y=0.40)  
    StaticSystem.add_node(x=1.30, y=0.40, Fx=5, Fy=-12)  

    ### add the elements to the system
    StaticSystem.add_element(start_node=1, end_node=2)  
    StaticSystem.add_element(start_node=1, end_node=3)  
    StaticSystem.add_element(start_node=3, end_node=2)  
    StaticSystem.add_element(start_node=2, end_node=4)  
    StaticSystem.add_element(start_node=3, end_node=4)  
    """
    def __init__(self):
        self.number_of_nodes = 0
        self.number_of_elements = 0
        self.list_of_nodes = []
        self.list_of_elements = []

    def add_node(self,
                 x: float,
                 y: float,
                 x_dof: DegreeOfFreedom = DegreeOfFreedom.MOVABLE,
                 y_dof: DegreeOfFreedom = DegreeOfFreedom.MOVABLE,
                 Fx: float = 0.0,
                 Fy: float = 0.0
                 ) -> None:
        """
        # add node
        ## purpose
        Adds a node to the static system: starting with node 1.

        ## overlapping nodes are allowed!
        The add_node() method does not check if a node with matching coordinates already exists.  
        This is on purpose, because:
        - All real 3D systems need to be simplified for a 2D system.
        - The simplified truss system can have overlapping nodes, that are
        completely independent of one another.

        Args:
            x: x-coordinate of the node
            y: y-coordinate of the node
            x_dof: the node can be movable or fixed in x-axis
            y_dof: the node can be movable or fixed in y-axis
            Fx: horizontal force in [kN]
            Fy: vertical force in [kN]
        """
        self.number_of_nodes += 1
        new_node = Node(
            number=self.number_of_nodes,
            x=float(x),
            y=float(y),
            x_dof=check_dof_input(x_dof),
            y_dof=check_dof_input(y_dof),
            Fx=float(Fx),
            Fy=float(Fy)
            )
        self.list_of_nodes.append(new_node) # add the new node to the list
        return None

    def add_element(self,
                    start_node: int,
                    end_node: int,
                    E=210000000.0,
                    A=0.02
                    ) -> None:
        """
        Adds an element to the static system: starting with element 1.
        Args:
            start_node: number of the first node of the element
            end_node: number of the first node of the element
            E: modulus of elasticity in [kN/m2]
            A: cross section area in [m2]
        """
        # try to get the node (list_of_nodes must be sorted and long enough)
        try:
            node1 = self.list_of_nodes[start_node-1]
            node2 = self.list_of_nodes[end_node-1]
            self.number_of_elements += 1
            new_element = TrussElement2D(
                number=self.number_of_elements,
                start_node=node1,
                end_node=node2,
                E=E,
                A=A
                )
            self.list_of_elements.append(new_element)
        except:
            row1 = f"Node {start_node} and node {end_node} do not exist in the list.\n"
            row2 = "Please add all nodes before adding an element."
            ValueError(row1 + row2)
        return None

    def save_static_system_as_pdf(self) -> None:
        """
        # save static system as pdf
        - saves the static system as a pdf
        """
        x_coords = []
        y_coords = []
        for node in self.list_of_nodes:
            x_coords.append(node.x)
            y_coords.append(node.y)
        fig, ax = plt.subplots()

        DIAMETER = ((max(x_coords)-min(x_coords))**2 + (max(y_coords)-min(y_coords))**2)**0.5 # for scaling

        # draw nodes
        ax.scatter(x_coords, y_coords, s=15, marker="o", color="black")

        # draw elements
        for element in self.list_of_elements:
            x1 = element.start_node.x
            x2 = element.end_node.x
            y1 = element.start_node.y
            y2 = element.end_node.y

            ax.plot([x1, x2], [y1, y2], color="black", linewidth=1)
        
        # draw loads
        for node in self.list_of_nodes:
            x, y = node.x, node.y

            # draw x-loads
            if node.Fx < 0:
                ax.arrow(x, y, dx=-DIAMETER/10, dy=0, head_width=DIAMETER/50)
            elif node.Fx > 0:
                ax.arrow(x, y, dx=DIAMETER/10, dy=0, head_width=DIAMETER/50)

            # draw y-loads
            if node.Fy < 0:
                ax.arrow(x, y, dx=0, dy=-DIAMETER/10, head_width=DIAMETER/50)
            elif node.Fy > 0:
                ax.arrow(x, y, dx=0, dy=DIAMETER/10, head_width=DIAMETER/50)

        # draw supports
        for node in self.list_of_nodes:
            print("...")
        
        ax.set_aspect("equal")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        fig.savefig("static_system.pdf")
        return None



