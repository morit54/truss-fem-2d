from src.truss_fem_2d import DegreeOfFreedom, StaticSystem, LinearTrussSolver


# CREATE A STATIC SYSTEM
SYSTEM = StaticSystem()

# NODES
SYSTEM.add_node(x=0.00, y=0.00, x_dof=DegreeOfFreedom.FIXED, y_dof=DegreeOfFreedom.FIXED) # Node 1
SYSTEM.add_node(x=0.90, y=0.00, x_dof=DegreeOfFreedom.FIXED, y_dof=DegreeOfFreedom.FIXED) # Node 2
SYSTEM.add_node(x=0.70, y=0.40) # Node 3
SYSTEM.add_node(x=1.30, y=0.40, Fx=5, Fy=-12) # Node 4

# ELEMENTS
SYSTEM.add_element(start_node=1, end_node=2)
SYSTEM.add_element(start_node=1, end_node=3)
SYSTEM.add_element(start_node=3, end_node=2)
SYSTEM.add_element(start_node=2, end_node=4)
SYSTEM.add_element(start_node=3, end_node=4)

# SOLVE THE SYSTEM
SOLVER = LinearTrussSolver(SYSTEM)

# SHOW THE RESULTS


matrix = SOLVER.displacements
print(matrix)



