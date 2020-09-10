""" ---------------------------------------------------------------------- """
import os
import csv
import numpy as np
import xlsxwriter
from xlrd import open_workbook
""" ---------------------------------------------------------------------- """

def create_datastruct(include_units=True):
    """
    Parameters:
    -----------
    include_units: boolean
        By default set to True. This will include a units keys to the GPS
        data structure containing parameter and unit pairs

    Returns:
    --------
    loc_data: dict
        Returns a GPS data structure in the form of nested dictionaries
        Where the first set of key contain 'activities' and 'units' keys

        The 'activities' dictionary contains a dictionary where it is 
        expected that key values pairs will be added in the following format
        
        {'activities': {'Act_1': {'Param_1': np.array([]), 'Param_2': np.array([]), ...}, 
                       {'Act_2': {'Param_1': np.array([]), 'Param_2': np.array([]), ...},
                       ...}
        
    Notes:
    ------
    List of parameters units to add include:
        * altitude, enhanced_altitude, position_lat, position_long, speed,
          enhanced_speed, distance, heart_rate, timestamp
    """

    loc_data = {'activities': {}}

    if include_units:
        loc_data['units'] = {'altitude':  'None',    'enhanced_altitude':  'm',
                             'speed':     'None',    'enhanced_speed':     'm/s',
                             'distance':  'm',       'heart_rate':         'bpm',
                             'timestamp': 'None',    
                             'position_lat': 'semicircles',   
                             'position_long':'semicircles'}

    return loc_data
    
def write_xlsx(loc_data,new_dir):
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

    new_dir: str
        Directory name to create, ensure it does not already exists
        This function only works in the current working directory

    Returns:
    --------
    None

    Notes:
    ------

    """

    # check if directory already exists
    try: 
        os.mkdir("./"+new_dir)
        os.rmdir("./"+new_dir)
    except FileExistsError:
        exp_str_out = "Directory '{}' already exists".format(new_dir)
        print(exp_str_out)
        return None
        
    workbook = xlsxwriter.Workbook("activities.xlsx")

    sheet_list = loc_data['activities'].keys()

    print("Writing to /{}/activities.xlsx".format(new_dir))

    for sh in sheet_list:
        print("\tWriting activity {}".format(sh))
        row, col = 0, 0
        worksheet = workbook.add_worksheet(sh)
        for key in loc_data['activities'][sh].keys():
            worksheet.write(row, col, key)
            worksheet.write_column(row+1, col, loc_data['activities'][sh][key])
            col += 1

    with open("units.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in loc_data['units'].items():
            writer.writerow([key,value])

    workbook.close()

    # move things around
    os.mkdir("./"+new_dir)
    os.rename("activities.xlsx","./{}/activities.xlsx".format(new_dir))
    os.rename("units.csv","./{}/units.csv".format(new_dir))

    return None

def read_xlsx(n_dir,fname=None,activities=None):
    """
    Parameters:
    -----------
    n_dir: str
        Directory name to read
        The directory must be present in the current working directory

    fname: str
        Specific excel file to read
        Following the write_xlsx() fuction, the default will be to read
        both the 'activites' and 'units' files

    activities: list
        List of desired parameter names to read as strings
        If None, all parameters will be read

    Returns:
    --------
    loc_data: dict
        Returns a GPS data structure in the form of nested dictionaries
        Where the first set of keys contain 'activities' and 'units' keys,
        unless if stated differently by fname.

        The 'activities' dictionary contains a dictionary containing the 
        parameter names as keys and parameter data as values in the form of
        numpy arrays
        
        {'activities': {'Act_1': {'Param_1': np.array([]), 'Param_2': np.array([]), ...}, 
                       {'Act_2': {'Param_1': np.array([]), 'Param_2': np.array([]), ...},
                       ...}

    Notes:
    ------

    """

    loc_data = {'activities': {}, 'units': {}}

    # read csv file containing units
    cwd = os.getcwd()
    with open(cwd+"/"+n_dir+"/units.csv") as csv_file:
        reader = csv.reader(csv_file)
        loc_data['units'] = dict(reader)

    # read excel file containing activities
    xls = open_workbook(cwd+'/'+n_dir+"/activities.xlsx")

    if isinstance(activities,(list)):
        sheets = activities
    else:
        sheets = xls.sheet_names()

    for sh in sheets:
        sheet = xls.sheet_by_name(sh)
        loc_data['activities'][sh] = {}
        for col_index in range(sheet.ncols):
            # for row_index in range(1, sheet.nrows):
            loc_data['activities'][sh][sheet.cell(0, col_index).value ] = np.array(sheet.col_values(col_index,start_rowx=1))
        
    return loc_data