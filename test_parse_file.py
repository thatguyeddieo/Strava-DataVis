from format import parse_file
from format import format

import matplotlib.pyplot as plt
import glob
import os
from datetime import datetime
from matplotlib.animation import FuncAnimation

import importlib 
importlib.reload(format)

# specify directory and parse fit.gz files
files_dr = glob.glob("*.fit.gz")
for f in files_dir:
    parse_file.parse(s_data,f)

# write out to folder
out_dir = "new_dataset"    
format.write_xlsx(s_data,out_dir)

# strava_data = format.read_xlsx(out_dir)

import numpy as np
# t = strava_data['activities']['4205465791']['timestamp']

# e_time = timestamp - timestamp[0]
for ij in strava_data['activities'].keys():
    t = strava_data['activities'][ij]['timestamp']
    strava_data['activities'][ij]['e_time'] = t - t[0]

# format.write_xlsx(strava_data,"append_df")

# fig, ax = plt.subplots(figsize=(10,10))

act = '4205465791'
e_time = strava_data['activities'][act]['e_time']
speed = strava_data['activities'][act]['enhanced_speed']
lat = strava_data['activities'][act]['position_lat']
long = strava_data['activities'][act]['position_long']



img = plt.imread("seattle500x500.png")
fig,ax = plt.subplots()
ax.imshow(img, zorder=0,extent=[-122.43479368847657*(2**31)/180 ,  -122.26313231152345*(2**31)/180,47.62217770739337*(2**31)/180, 47.737752285340434*(2**31)/180])
# print(min(long))
# x_min = -122.43479368847657*(2**31)/180
# x_max = -122.26313231152345*(2**31)/180
# print(-122.43479368847657*(2**31)/180 )
# ax.imshow(img, zorder=0,extent=[min(long),max(long),min(lat),max(lat)])
ax.set_aspect(aspect=1.5)
ax.set_xlim(-122.43479368847657*(2**31)/180 ,  -122.26313231152345*(2**31)/180) 
ax.set_ylim(47.62217770739337*(2**31)/180, 47.737752285340434*(2**31)/180) #added
ax.plot(long,lat,zorder=1)
plt.show()


