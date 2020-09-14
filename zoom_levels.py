from formats import formats
import matplotlib.pyplot as plt
import numpy as np
from calcs import convert
from utils import mapCalcs
from calcs import limits
from matplotlib.animation import FuncAnimation
import requests
import os

import importlib 
importlib.reload(formats)
importlib.reload(mapCalcs)
importlib.reload(convert)
importlib.reload(limits)

# load dateset from folder
read_dir = "Interpolated_Dataset"
# strava_data = formats.read_xlsx(read_dir)

map_width,map_height = 500,500
center = convert.units('deg_to_semi',[-122.373471,47.695239]) # parla in [long,lat] coords!!!!

fram_size = np.arange(15, 8, -1)
internal_size = 1500 # smaller is faster
colors = iter(['red','black','blue','green','yellow']*100)

fig, ax = plt.subplots(figsize=(10,10))

plt_coord, = plt.plot([],[],'ro',markersize=10)
ax.set_xticks([])
ax.set_yticks([])
def get_gm_image(zm,sc,cen):

    gm_url = "https://maps.googleapis.com/maps/api/staticmap?"
    cen = convert.units('semi_to_deg',cen)
    center_gm = "{}, {}".format(cen[1],cen[0])
    
    api_path = "/Users/eddiebunzo/Desktop/Python/google_api_key.txt"
    with open(api_path) as a:
        api_key = a.readline()

    img_out = 'maps_n_gifs/seattlezm{}scale{}500x500.png'.format(zm,sc)
    if os.path.exists(img_out):
        print('breaking gm loop')
        return img_out

    url = gm_url +"center=" + center_gm + "&zoom=" + str(zm) + "&size=500x500&scale="+str(sc)+"&key=" + api_key
    response = requests.get(url) 

    # storing the response in a file (image)

    with open(img_out, 'wb') as file:
        # writing data into the file
        file.write(response.content) 

    return img_out
    
def animate(i):
    color = next(colors)
    zoom = i
    scale = 4
    title = "Center = ({} long,{} lat)\n".format(center[1],center[0]) +\
            "Zoom = {}  Scale = {}".format(i,scale)

    img_file = get_gm_image(zoom,scale,center)

    img = plt.imread(img_file)
    int_corners = mapCalcs.get_corners(zoom,center,[map_width,map_height],
                        in_coord_units='semi',out_coord_units='semi')
    ax.imshow(img, zorder=0,extent=[int_corners[3],int_corners[1],int_corners[2],int_corners[0]])
    ax.set_aspect(aspect=1.5)

    # ax = plt.axis([0,2*np.pi,-1,1])
    print(int_corners)
    ax.set_xlim([int_corners[3],int_corners[1]])
    ax.set_ylim([int_corners[2],int_corners[0]])
    ax.scatter(center[0],center[1],s=i,color='Black',marker='^')
    ax.plot([int_corners[3],int_corners[3]],[int_corners[2],int_corners[0]],color=color)
    ax.plot([int_corners[1],int_corners[1]],[int_corners[2],int_corners[0]],color=color)
    ax.plot([int_corners[3],int_corners[1]],[int_corners[2],int_corners[2]],color=color)
    ax.plot([int_corners[3],int_corners[1]],[int_corners[0],int_corners[0]],color=color)
    ax.set_title(title)
    
    return plt_coord,

# # create animation using the animate() function
myAnimation = FuncAnimation(fig, animate, frames=fram_size, \
                                      interval=internal_size, blit=True, repeat=True)
myAnimation.save('maps_n_gifs/map_scale_4.gif', writer='imagemagick',fps=0.5)

plt.show()