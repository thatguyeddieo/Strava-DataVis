import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from calcs import convert
from utils import mapCalcs
from utils import googleAPI

# center at green lake [long,lat]
center = convert.units('deg_to_semi',[-122.338024,47.677978])
colors = iter(['black','blue','orange','green','red']*20)

fig, ax = plt.subplots(figsize=(10,10))
plt_coord = plt.plot([],[],'ro')
ax.set_xticks([])
ax.set_yticks([])

# get API key, add your own Google API Key here 
# see utils.googleAPI() module for more info
api_path = "/Users/eddiebunzo/Desktop/Python/google_api_key.txt"
with open(api_path) as a:
    api_key = a.readline()

def animate(i):
    color = next(colors)
    
    # set static map props
    map_width,map_height = 500,500
    zoom, scale = i, 4
    title = "Zoom = {},  Scale = {}\n".format(i,scale) +\
            "Center = Green Lake,  WxH = 500x500"
    img_fname = 'GreenLake&Zm{}&Scale{}&Size500x500'.format(zoom,scale)

    # convert to degrees to use in googleAPI module
    cent_gm = convert.units('semi_to_deg',center)

    # get static map
    img_loc = googleAPI.get_map(zoom,scale,[cent_gm[1],cent_gm[0]],
                    api_key,img_fname,check=True,out_dirc='maps_n_gifs_dev')

    # get generated map corners and edges
    int_corners = mapCalcs.get_corners(zoom,center,[map_width,map_height],
                        in_coord_units='semi',out_coord_units='semi')

    # plot map on matplotlib figure
    img = plt.imread(img_loc)
    ax.imshow(img, zorder=0,extent=[int_corners[3],int_corners[1],int_corners[2],int_corners[0]])
    ax.set_aspect(aspect=1.5)

    # set limits
    ax.set_xlim([int_corners[3],int_corners[1]])
    ax.set_ylim([int_corners[2],int_corners[0]])

    # add central location marker
    ax.scatter(center[0],center[1],s=i,color='Black',marker='^')

    # add box limits to illustrate zoom level
    ax.plot([int_corners[3],int_corners[3]],[int_corners[2],int_corners[0]],color=color)
    ax.plot([int_corners[1],int_corners[1]],[int_corners[2],int_corners[0]],color=color)
    ax.plot([int_corners[3],int_corners[1]],[int_corners[2],int_corners[2]],color=color)
    ax.plot([int_corners[3],int_corners[1]],[int_corners[0],int_corners[0]],color=color)

    ax.set_title(title)
    
    return plt_coord

# interval, smaller is faster
zoom_levels = np.arange(16, 8, -1)
myAnimation = FuncAnimation(fig, animate, frames=zoom_levels, \
                                      interval=1125, blit=True, repeat=True)

# save gif
myAnimation.save('maps_n_gifs_dev/GreenLake_Zoom_Scale_4.gif', writer='imagemagick')
