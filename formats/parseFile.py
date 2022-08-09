""" ---------------------------------------------------------------------- """
import gzip
import fitparse
import numpy as np
from datetime import datetime
""" ---------------------------------------------------------------------- """

def parse(loc_data,fn):
    """
    Parameters
    -----------
    loc_data: dict
        GPS data structure in the form defined by the formats package docstring
        Only containing the first set of 'activities' and 'units' keys
        
    fn: str
        Gzip file name containing compressed .fit file

    Returns
    --------
    None

    Notes
    ------
    This function will add to loc_data['activities'] by including the .fit
    file's parameters and values. In the same format as defined in the 
    formats package docstring.

    {'activities': {'Act_1': {'Param_1': np.array([]), 'Param_2': np.array([]), ...}, 
                    {'Act_2': {'Param_1': np.array([]), 'Param_2': np.array([]), ...},
                    ...}

    The list of parameters to parse include:
        * altitude
        * enhanced_altitude
        * position_lat
        * position_long
        * speed
        * enhanced_speed
        * distance
        * heart_rate
        * timestamp
                
        Note to developers:
        Make more robust by checing if file is gzip or fit.
        Check to see if dictionary was already created which contains
        activity and unit keys
        
    """

    try:
        loc_data['activities']

    except KeyError:
        ex_str_out = "Key 'activities' does not exist in dictionary\n" +\
                     "passed. Create a data structure as defined in\n" +\
                     "format.format.create_datastr()\n\n"
        print(ex_str_out)
        return 

    print("Parsing " + fn +"...") 

    with gzip.open(fn) as n:
        # split filename from directory 
        f_split = fn.split("/")
        
        fit_key = f_split[-1][:-7]
        fitfile = fitparse.FitFile(n)

        # Default parameters to track
        loc_data['activities'][fit_key] = {'altitude':[],       'enhanced_altitude':[],
                                           'position_lat': [],  'position_long':[],
                                           'speed':[],          'enhanced_speed':[],
                                           'distance':[],       'timestamp':[]}
        
        for record in fitfile.get_messages("record"):
            # by checking if len(record.fields) >= 8 the function will pull out data containing at least 8 parameters
            # which may or may not match the parameters listed above.
            if len(record.fields) >= 8:
                for data in record:
                    if str(data.name) in loc_data['activities'][fit_key].keys():
                        if data.name == 'timestamp':
                            loc_data['activities'][fit_key][str(data.name)].append(datetime.timestamp(data.value))
                        else:
                            loc_data['activities'][fit_key][str(data.name)].append(data.value)

        for k in loc_data['activities'][fit_key].keys():
            # check to see if list is empty
            if not loc_data['activities'][fit_key][k]:
                error_out = "\tWarning: Parameter {} was not populated with data.".format(k)
                print(error_out)
                
    return None
