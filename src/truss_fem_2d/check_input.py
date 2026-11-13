from .node import DegreeOfFreedom

def check_dof_input(input: any):
    """
    # check dof input of a node
    ## purpose
    - checks if the given input is a DegreeOfFreedom object
    - this function will try to convert a string into a DegreeOfFreedom object
     by using DegreeOfFreedom("input")
    """
    # check the type
    if isinstance(input, DegreeOfFreedom):
        return input
    else:
        try:
            input = DegreeOfFreedom(input)
            return input
        except:
            row1 = "The given input cannot be converted to a DegreeOfFreedom object.\n"
            row2 = f"Please adjust the {input} value."
            raise ValueError(row1 + row2)


