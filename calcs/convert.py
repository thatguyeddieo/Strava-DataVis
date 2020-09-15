""" ---------------------------------------------------------------------- """
import math
import numpy as np
""" ---------------------------------------------------------------------- """

def units(c_type,vals):
    """
    Parameters
    -----------
    c_type: str
        String containing conversion type
        See unit_type.keys() for available conversions. If a non valid
        conversion type is passed this function will return an error message
        and None

    vals: np.ndarray, float, int, list
        Data to convert

    Returns
    --------
    np.ndarray, float, int
        Returns new converted data in the same data type as what was
        passed in vals

    Examples
    ---------
    >>> import numpy as np
    >>> print('Hello World')
    Hello World
    """
    unit_type = {'deg_to_semi':     lambda x: x*(2**31)/180,
                 'semi_to_deg':     lambda x: x*180/(2**31),
                 'deg_to_rad':      lambda x: x*(math.pi/180),
                 'rad_to_deg':      lambda x: x/(math.pi/180)}

    if isinstance(vals,(np.ndarray,float,int,list)):
        if isinstance(vals,list):
            vals = np.array(vals)
        if c_type not in unit_type:
            str_out = "{} not a valid conversion type\n" +\
                      "See calcs.convert.units() for available conversions"
            print(str_out.format(c_type))
            return None

        convert_result = unit_type[c_type](vals)
        
    else:
        str_out = "Check values passed, function units() takes either\n" +\
                  "list, float value or floats within a numpy array."
        print(str_out)

    return convert_result
    