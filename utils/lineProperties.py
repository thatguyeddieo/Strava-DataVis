""" ---------------------------------------------------------------------- """
import numpy as np
from matplotlib.collections import LineCollection
""" ---------------------------------------------------------------------- """

def add_points(lc,point,num_points,rgba):
    """
    Parameters
    -----------
    lc: LineCollection
        
    point: list, np.ndarray
        Point to add to LineCollection lc
        Must be a single point in the form [x,y]

    num_points: int
        Number of points to display. As more than num_points get
        added to LineCollection lc, the function will display the 
        most recent num_points points

    rgba: np.ndarray
        Red, green, blue, alpha color matrix. Should be a 2D array
        with shape (num_points,4). See get_colors() for more 
        information

    Returns
    --------
    None
    Notes
    -----
    Function returns None but sets LineCollection lc's segments
    and colors. The segments are added as a 3D array of size 
    (num_points,2,2). See the example below in Examples

    lc's colors are set using the rgba parameter
    
    Examples
    --------
    >>> line = LineCollection([])
    >>> n_points, tail_length = 10, (3/4.)*n_points
    >>> rgb_color = [0.0, 0.5, 1.0]
    >>> tip_color = [1.0, 0.0, 0.0]
    >>> rgba_color = lineProp.define_colors(n_points,tail_length,
                                            rgb_color,tip_color)
    >>> for i in range(10):
    >>>     lineProp.add_points(line,[i,i],n_points,rgba_color) 
    >>> print("Line Segments: ",line.get_segments())
    Line Segments: 
    [array([[0., 0.], [0., 0.]]), 
     array([[0., 0.], [1., 1.]]), 
     array([[1., 1.], [2., 2.]]), 
     array([[2., 2.], [3., 3.]]), 
     array([[3., 3.], [4., 4.]]), 
     array([[4., 4.], [5., 5.]]), 
     array([[5., 5.], [6., 6.]]), 
     array([[6., 6.], [7., 7.]]), 
     array([[7., 7.], [8., 8.]]), 
     array([[8., 8.], [9., 9.]])]

    """

    if not isinstance(lc,LineCollection):
        str_out = "Pass parameter lc as LineCollection object\n" +\
                  "by using matplotlib.collections and LineCollection([]) "
        print(str_out)
        return None
    
    if isinstance(point,list):
        point = np.array(point)

    # Check to see if point contains only one pair
    if len(point.shape) > 1:
        str_out = "This function is meant to take only one point\n" +\
                  "User passed point as: \n{}".format(point)
        print(str_out)
        return None

    pre_segments = lc.get_segments()

    if len(pre_segments) == 0:
        reshape_points = np.array([point,point]).T.reshape(-1, 1, 2)
        new_segments = np.concatenate([reshape_points[:-1], 
                                       reshape_points[1:]],axis=1)
            
    elif len(pre_segments) < num_points:
        new_segments = np.concatenate((pre_segments,
                                     [[pre_segments[-1][1],point]]))

    else:
        new_segments = np.concatenate((pre_segments[1:],
                                     [[pre_segments[-1][1],point]]))
    
    if new_segments.shape[0] < num_points:
        short_rgba = rgba[-new_segments.shape[0]:]
        lc.set_segments(new_segments)
        lc.set_color(short_rgba)
        return None
    
    lc.set_segments(new_segments)
    lc.set_color(rgba)
    return None

def define_colors(num_points,tail_len,rgb,rgb_tip):
    """
    Parameters
    -----------
    num_points: int
        Number of points to display. As more than num_points get
        added to LineCollection lc, the function will display the 
        most recent num_points points

    tail_len: float, int
        The portion of segments to be considered as the tail. The
        tail will be faded out by reducing their alpha values

    rgb: list, np.ndarray
        [Red, Green, Blue] color mapping to use for the line 

    rgb_tip: list, np.ndarray
        [Red, Green, Blue] color mapping to use for the tip
        The tip in this case is define as the first 5 points

    Returns
    --------
    rgba: 
        Red, green, blue, alpha color matrix. Returned as a 2D array
        with shape (num_points,4). Where each row is a point. While the 
        first three columns represent the Red, Green, Blue (RGB) shades,
        and the last column represents the alpha values associated with 
        each point. See example below
        
    Examples
    --------
    >>> n_points, tail_length = 10, (3/4.)*n_points
    >>> rgb_color = [0.0, 0.5, 1.0]
    >>> tip_color = [1.0, 0.0, 0.0]
    >>> rgba_color = lineProp.define_colors(n_points,tail_length,
                                            rgb_color,tip_color)
    >>> print("Rgba Matrix: ",rgba_color)
    >>> alphas = rgba_color[:,3]
    >>> print("Alphas: : ",alphas)
    RGBA Matrix: 
    [[0.         0.5        1.         0.14285714]
     [0.         0.5        1.         0.28571429]
     [0.         0.5        1.         0.42857143]
     [0.         0.5        1.         0.57142857]
     [0.         0.5        1.         0.71428571]
     [1.         0.         0.         0.85714286]
     [1.         0.         0.         1.        ]
     [1.         0.         0.         1.        ]
     [1.         0.         0.         1.        ]
     [1.         0.         0.         1.        ]]
    Alphas: : 
    [0.14285714 0.28571429 0.42857143 0.57142857 0.71428571 0.85714286
    1.         1.         1.         1.        ]

    """

    if isinstance(tail_len,float):
        tail_len = int(tail_len)

    rgba = np.zeros((num_points,4))
    rgba[:-5,:3] = rgb
    rgba[-5:,:3] = rgb_tip

    # set alphas to tail and head
    tail = np.linspace(1/tail_len,1,tail_len)
    head = np.ones(num_points-tail_len)
    alphas = np.concatenate((tail,head))

    rgba[:,3] = alphas

    return rgba