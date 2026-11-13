from math import floor, ceil

def num_round(num: float, k: int) -> str:
    """
    # num round
    - rounds a number to k decimal places
    - returns the number as a string
    - replaces the "." with a ","
    
    ## example
    The number 2.5 rounded to k=2 decimal places will return "2,50"
    """
    factor = 10**k
    a = num * factor

    if a - floor(a) >= 0.5:
        a = ceil(a)
    else:
        a = floor(a)
    
    rounded_str = str(a / factor)
    zeros = k - len(rounded_str.split(".")[1])
    string_number =  rounded_str + "0"*zeros
    return string_number.replace(".", ",")