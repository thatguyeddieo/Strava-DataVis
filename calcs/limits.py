""" ---------------------------------------------------------------------- """
import math
import numpy as np
""" ---------------------------------------------------------------------- """

def check_bounds(d,min_val,max_val):
    """
    Parameters
    -----------
    d: list or ndarray
        Values to analysis

    min_val: float or int
        Lower bound to check against

    max_val: float or int
        Upper bound to check against

    Returns
    --------
    boolean
        Where True is returned if the values in parameter d do not 
        exceed the bounds. And False is returned if at least one value 
        in parameter d exceeds the min or max bounds

    Examples
    --------
    >>> import numpy as np
    >>> int_lst = [np.random.random() for i in range(0,5)]
    >>> res = limits.check_bounds(int_lst,min_val=0.25,max_val=0.75)
    >>> print(int_lst,res)
    [0.74902032324641, 0.693027036057998, 0.3161441813761138, 
     0.30559690839814946, 0.348190216012778] True

    """

    if isinstance(d,(list,np.ndarray)):
        if isinstance(d,list):
            d = np.array(d)
        if isinstance(d[0],np.ndarray):
            d = np.concatenate(d).ravel()
        res_bool = np.logical_or(d < min_val, d > max_val)
        res = sum(res_bool)

        if not res:
            return True
            
        return False

    str_out = "Pass either a list or np.ndarray data type\n"
    print(str_out)

    return None