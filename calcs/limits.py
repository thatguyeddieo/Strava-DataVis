""" ---------------------------------------------------------------------- """
import math
import numpy as np
""" ---------------------------------------------------------------------- """

def check_bounds(d,min_val,max_val):
    """
    Parameters:
    -----------
    d: list or ndarray
        Values to analysis

    min_val: float or int
        Lower bound to check against

    max_val: float or int
        Upper bound to check against
    Returns:
    --------
    boolean
        Where True is returned if the values in parameter d do not 
        exceed the bounds. And False is returned if at least one value 
        in parameter d exceeds the min or max bounds

    Notes:
    ------

    """

    if isinstance(d,(list,np.ndarray)):
        if isinstance(d[0],np.ndarray):
            d = np.concatenate(d).ravel()
        res_bool = np.logical_or(d < min_val, d > max_val)
        res = sum(res_bool)

        if not res:
            return True
            
        return False

    return None