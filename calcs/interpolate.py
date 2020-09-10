""" ---------------------------------------------------------------------- """
import numpy as np
from scipy import interpolate
""" ---------------------------------------------------------------------- """

def intrp1d(loc_data,new_parm,params,step_size,activities='All',kind='linear'):
    """
    Parameters:
    -----------
    loc_data: dict
        GPS data structure in the form defined by the formats package docstring
        Dict of activities, their parameters and values:
        loc_data: {'Activities': {'Act_1': {'Speed': np.array([1,2,3... ]), ... } 
                                  'Act_2': {'Speed': np.array([1,2,3... ]), ... }
                                  ...} 
                    'Units': ...}

    new_parm: str
        New parameter name which will be added to the GPS data structure

    params: list
        List of parameters to use for interpolation
        Where the first index contains a string naming the independent parameter
        and the second index contains a string naming the dependent parameter

        Exampe:  ['Time','Speed']
                   Time = Independent variable
                   Speed = Dependent variable

    step_size: float, int
        The first and last data point from the independent paramter along with
        the step size parameter will be used to create a new independent
        parameter for interpolation

    activity: str, list
        By default a string value adding interpolation results to all activities.
        Pass list to specify an activity or activities

    kind: str or int
        From scipy documentation:
        Specifies the kind of interpolation as a string (‘linear’, ‘nearest’, 
        ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’,
        where ‘zero’, ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline 
        interpolation of zeroth, first, second or third order; ‘previous’ and 
        ‘next’ simply return the previous or next value of the point) or as an 
        integer specifying the order of the spline interpolator to use. Default 
        is ‘linear’.

    Returns:
    --------
    loc_data
        Data structure containing a

    Notes:
    ------
    None
    
    """

    # check that only one indp variable was passed
    if len(params) != 2:
        str_out = "Check that params contains only independent and\n" +\
                  "dependent variables in that order.\n" +\
                  "User passed:  params = {}\n".format(params) +\
                  "Expected:     params = ['ind var','dep var']\n\n"
        print(str_out)
        return None

    # tuples work
    if isinstance(params,tuple):
        params = list(params)

    if isinstance(activities,list):
        activs = activities
    elif activities == 'All':
        activs = [i for i in loc_data['activities'].keys()]

    for a in activs:
        act_parms = loc_data['activities'][a]

        x_new = np.arange(start=act_parms[params[0]][0],
                          stop=act_parms[params[0]][-1],
                          step=step_size)
        
        int_func = interpolate.interp1d(act_parms[params[0]],
                                        act_parms[params[1]],kind=kind)

        new_func = int_func(x_new)

        loc_data['activities'][a][new_parm] = new_func
        loc_data['activities'][a]['{}_intrp'.format(params[0])] = x_new
        
    return None