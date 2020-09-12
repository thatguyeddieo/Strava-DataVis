""" ---------------------------------------------------------------------- """
import math
import numpy as np
from calcs import convert
""" ---------------------------------------------------------------------- """

def get_center(loc_data,coord,coord_keys,conversion=None):
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

    coord: int or range
        Coordinates to index 

    coord_keys: list
        Coordinate parameter names as strings
        where longitude is the first string and latitude is the second

    conversion: None, str
        By default set to None, user can provide conversion string to use
        in accordance with module calcs.convert.units() and its available
        conversion types

    Returns: 
    --------
    center_coords: ndarray
        Returns calculated center coordinates as shown below:
        [long_center_coord,lat_center_coord]

    Notes:
    ------

    """

    # check to see if keys exists in data strcutures
    try: 
        acts = [a for a in loc_data['activities'].keys()]
        loc_data['activities'][acts[0]][coord_keys[0]]
        loc_data['activities'][acts[0]][coord_keys[1]]

    except KeyError:
        str_out = "One key in pair {} does not exists in data structure.\n" +\
                  "Exiting get_center() function and returning [nan,nan] coordinates\n"
        print(str_out.format(coord_keys))
        return [np.nan,np.nan]

    if isinstance(coord,range):
        print(coord)
        strt, end = coord[0], coord[-1]
        coords = slice(strt,end)
    elif isinstance(coord,int):
        strt, end = coord, coord+1
        coords = slice(strt,end)
    else:
        print('Error Message')
        return None

    act_parms = loc_data['activities']
    coords_array0 = [list(act_parms[a][coord_keys[0]][coords])
                     for a in act_parms.keys()
                     if end < len(act_parms[a][coord_keys[0]])]
    coords_array1 = [list(act_parms[a][coord_keys[1]][coords])
                     for a in act_parms.keys()
                     if end < len(act_parms[a][coord_keys[1]])]

    center_coords = np.mean([sum(coords_array0,[]),sum(coords_array1,[])],axis=1)

    if isinstance(conversion,str): 
        return convert.units(conversion,center_coords)
    else:
        return center_coords
    
def get_corners(zoom,center,widxhght,in_coord_units='degrees',out_coord_units='degrees'):
    """
    Parameters:
    -----------
    zoom: int
        Zoom level of the region desired

    center: list, ndarray
        center coordinates in list or numpy array form
        [long_coord, lat_coord] 
    
    widxhght: list, ndarray
        Defines the rectangular dimensions of the map. The parameter 
        takes a list of integers where the first value is the width 
        size and second is the height size

    in_coord_units: str
        This function calculates the corners by initizaling the center
        in degree units if non degree units are passed. The function 
        will use the in_coord_units string value to convert the data 
        from what is passed to degrees then perform the calculations. 
        Available options include:
            * 'semi'

    out_coord_units: str
        By default set to degrees, user can provide conversion string 
        to use in accordance with module calcs.convert.units() and 
        its available conversion types.
            * 'semi'
            
    Returns:
    --------
    corners: tuple
        Tuple containing the corners in the following order
        (n_lim, e_lim, s_lim, w_lim)

    Notes:
    ------
        Throughout this function x refers to longitude coordinates and
        y refers to latitude coordinates.

        The following constants are used to perform calculations
        mercator length:            256
        pixels per long degree:    (256/360)
        pixels per lonng radian:   (256/(2*math.pi))

    """

    if in_coord_units[:4] == 'semi':
        center = convert.units('semi_to_deg',center)

    scale = 2**zoom

    center_pxs = get_center_pxs(center)

    w_lim,s_lim = get_SW_point(scale,center_pxs,widxhght)
    e_lim,n_lim = get_NE_point(scale,center_pxs,widxhght)
    corners = (n_lim,e_lim,s_lim,w_lim)

    if out_coord_units[:4] == 'semi': 
        corners = convert.units('deg_to_semi',np.array([n_lim, e_lim, 
                                                        s_lim, w_lim]))
        return corners

    return corners

def get_center_pxs(center):
    """
    Parameters:
    -----------
    center: list, ndarray
        Center coordinates in list or numpy array form
        [long_coord, lat_coord] 
    
    Returns:
    --------
    point_x, point_y: float
        Center longitude and latitude coordinates in pixels

    Notes:
    ------
    
    """

    mercator_len = 256 
    mercator_origin_x, mercator_origin_y = [mercator_len/2]*2 

    center_x, center_y = center # unpack coords

    point_x = mercator_origin_x+center_x*(256/360)

    siny = math.sin(convert.units('deg_to_rad',center_y)) 
    point_y = mercator_origin_y+0.5 * math.log((1+siny) / 
              (1-siny)) * (-(256/(2*math.pi)))
   
    return point_x, point_y

def get_SW_point(scale,center_pxs,widxhght):
    """
    Parameters:
    -----------
    scale: float
        Map scale based on zoom level

    center_pxs: list, ndarray
        Center pixel coordinates in list or numpy array form
        [long_coord, lat_coord] 
    
    widxhght: list, ndarray
        Defines the rectangular dimensions of the map. The parameter 
        takes a list of integers where the first value is the width 
        size and second is the height size

    Returns:
    --------
    sw_lng, sw_lat: float
        Southwest corner coordinates in degrees
        [sw_long_coord, sw_lat_coord]

    Notes:
    ------
    Using the southwest coordinates the west and south map boundaries
    are known 
    """

    mercator_len = 256 
    mercator_origin_x, mercator_origin_y = [mercator_len/2]*2

    wid, hght = widxhght

    center_px_x, center_px_y = center_pxs
    sw_x, sw_y = ( center_px_x-(wid/2)/scale, center_px_y+(hght/2)/scale)

    sw_lng = (sw_x-mercator_origin_x)/(256/360)
    sw_lat_rads = (sw_y-mercator_origin_y)/(-1*((256/(2*math.pi)))) 
    sw_lat = convert.units('rad_to_deg',
                (2*math.atan(math.exp(sw_lat_rads))-math.pi/2)) 

    return sw_lng,sw_lat

def get_NE_point(scale,center_pxs,widxhght):
    """
    Parameters:
    -----------
    scale: float
        Map scale based on zoom level

    center_pxs: list, ndarray
        Center pixel coordinates in list or numpy array form
        [long_coord, lat_coord] 
    
    widxhght: list, ndarray
        Defines the rectangular dimensions of the map. The parameter 
        takes a list of integers where the first value is the width 
        size and second is the height size

    Returns:
    --------
    ne_lng, ne_lat: float
        Northeast corner coordinates in degrees
        [ne_long_coord, ne_lat_coord]
    Notes:
    ------
    Using the northeast coordinates the north and east map boundaries
    are known 
    """

    mercator_len = 256 
    mercator_origin_x, mercator_origin_y = [mercator_len/2]*2 

    wid, hght = widxhght 
    center_px_x, center_px_y = center_pxs 

    ne_x, ne_y = (center_px_x+(wid/2)/scale, center_px_y-(hght/2)/scale)

    ne_lng = (ne_x-mercator_origin_x)/(256/360) 
    ne_lat_rads = (ne_y-mercator_origin_y)/(-1*((256/(2*math.pi)))) 
    ne_lat = convert.units('rad_to_deg',
                (2*math.atan(math.exp(ne_lat_rads))-math.pi/2))

    return ne_lng,ne_lat
