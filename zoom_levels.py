import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from calcs import convert
from utils import mapCalcs
from utils import googleAPI

map_width,map_height = 500,500
center = convert.units('deg_to_semi',[-122.338024,47.677978])
colors = iter(['black','blue','orange','green','red']*20)

fig, ax = plt.subplots(figsize=(10,10))
plt_coord = plt.plot([],[],'ro')
ax.set_xticks([])
ax.set_yticks([])

# get API key    
api_path = "/Users/eddiebunzo/Desktop/Python/google_api_key.txt"
with open(api_path) as a:
    api_key = a.readline()

def animate(i):
    color = next(colors)
    zoom, scale = i, 4

    cent_gm = convert.units('semi_to_deg',center)
    title = "Zoom = {}  Scale = {}".format(i,scale)

    img_fname = 'GreenLake&Zm{}&Scale{}&Size500x500'.format(zoom,scale)

    img_loc = googleAPI.get_map(zoom,scale,[cent_gm[1],cent_gm[0]],
                    api_key,img_fname,check=True,out_dirc='maps_n_gifs_dev')
    
    img = plt.imread(img_loc)
    int_corners = mapCalcs.get_corners(zoom,center,[map_width,map_height],
                        in_coord_units='semi',out_coord_units='semi')
    
    ax.imshow(img, zorder=0,extent=[int_corners[3],int_corners[1],int_corners[2],int_corners[0]])
    ax.set_aspect(aspect=1.5)

    ax.set_xlim([int_corners[3],int_corners[1]])
    ax.set_ylim([int_corners[2],int_corners[0]])

    ax.scatter(center[0],center[1],s=i,color='Black',marker='^')

    ax.plot([int_corners[3],int_corners[3]],[int_corners[2],int_corners[0]],color=color)
    ax.plot([int_corners[1],int_corners[1]],[int_corners[2],int_corners[0]],color=color)
    ax.plot([int_corners[3],int_corners[1]],[int_corners[2],int_corners[2]],color=color)
    ax.plot([int_corners[3],int_corners[1]],[int_corners[0],int_corners[0]],color=color)
    ax.set_title(title)
    
    return plt_coord

# interval, smaller is faster
myAnimation = FuncAnimation(fig, animate, frames=np.arange(16, 8, -1), \
                                      interval=1250, blit=True, repeat=True)
myAnimation.save('maps_n_gifs_dev/map_test_scale_4.gif', writer='imagemagick',fps=0.5)
