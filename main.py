from src.truss_fem_2d import DegreeOfFreedom, StaticSystem, LinearTrussSolver


# CREATE A STATIC SYSTEM
SYSTEM = StaticSystem()

# NODES
SYSTEM.add_node(x=0, y=0, x_dof=DegreeOfFreedom.FIXED, y_dof=DegreeOfFreedom.FIXED)
SYSTEM.add_node(x=5, y=5, Fy=-10)
SYSTEM.add_node(x=15, y=0, x_dof=DegreeOfFreedom.FIXED, y_dof=DegreeOfFreedom.FIXED)

# ELEMENTS
SYSTEM.add_element(start_node=1, end_node=2)
SYSTEM.add_element(start_node=2, end_node=3)

# SOLVE THE SYSTEM
SOLVER = LinearTrussSolver(SYSTEM)

# SHOW THE RESULTS
matrix = SOLVER.normal_forces
print(matrix)





