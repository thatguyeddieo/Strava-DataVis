from formats import formats
import matplotlib.pyplot as plt
import numpy as np
from calcs import convert
from utils import mapCalcs
from calcs import limits

import importlib 
importlib.reload(formats)
importlib.reload(mapCalcs)
importlib.reload(convert)
importlib.reload(limits)

# load dateset from folder
read_dir = "Interpolated_Dataset"
strava_data = formats.read_xlsx(read_dir)


# map_center = [-122.348963,47.679997]
# zoom = 12
# mapWidth,mapHeight = 500, 500
# # centerPoint = MapPro.G_LatLng(centerLat, centerLon)
# # corners = MapPro.getCorners(centerPoint, zoom, mapWidth, mapHeight)
# # print(corners)
# print(mapCalcs.get_corners(zoom,map_center,[mapWidth,mapHeight]))
# lat_max, long_max, lat_min, long_min = mapCalcs.get_corners(zoom,map_center,[mapWidth,mapHeight])
# long_min_semi,long_max_semi = convert.units('deg_to_semi',np.array([long_min, long_max]))
# lat_min_semi,lat_max_semi = convert.units('deg_to_semi',np.array([lat_min, lat_max]))


# fig, ax = plt.subplots(figsize=(10,10))
# img = plt.imread("seattle500x500.png")
# ax.imshow(img, zorder=0,extent=[long_min_semi,long_max_semi,lat_min_semi,lat_max_semi])
# ax.set_aspect(aspect=1.5)
# ax.set_xlim(long_min_semi,long_max_semi)
# ax.set_ylim(lat_min_semi,lat_max_semi)
# for a in range(0,10000,1000):
#   x_ctr, y_ctr = mapCalcs.get_center(strava_data,a,['long_intrp','lat_intrp'])
#   plt.scatter(x_ctr,y_ctr)

# print(strava_data['activities'].keys())

# for i in strava_data['activities'].keys():
#     print(i)
#     lat = strava_data['activities'][i]['lat_intrp']
#     lng = strava_data['activities'][i]['long_intrp']

#     plt.scatter(lng,lat)

fig, ax = plt.subplots(figsize=(10,10))

zoom = 12
map_width,map_height = 500,500
colors = iter(['red','black','blue','green','yellow']*100)
for a in range(5,7000,500):
    color = next(colors)
    map_center = mapCalcs.get_center(strava_data,range(0,a),['long_intrp','lat_intrp'])
    print(map_center)
    lat_max, long_max, lat_min, long_min = mapCalcs.get_corners(zoom,map_center,[map_width,map_height],
                in_coord_units='semi',out_coord_units='semi')
    # ax.plot([long_min_semi,lat_min_semi],[long_min_semi,lat_max_semi])
    ax.plot([long_min,long_min],[lat_min,lat_max],color=color)
    ax.plot([long_min,long_max],[lat_max,lat_max],color=color)
    ax.plot([long_min,long_max],[lat_min,lat_min],color=color)
    ax.plot([long_max,long_max],[lat_min,lat_max],color=color)
    ax.scatter(map_center[0],map_center[1],c=color,s=100)
    long = [strava_data['activities'][i]['long_intrp'][:a] for i in strava_data['activities'].keys()]
    late = [strava_data['activities'][i]['lat_intrp'][:a]  for i in strava_data['activities'].keys()]

    print('long: ',long)
    print('lat: ',late)
    print('long_min: ',long_min)
    print('long_max: ',long_max)
    ax.scatter(long,late,c=color)
    chk_bounds = limits.check_bounds(long,long_min,long_max)
    if chk_bounds == False:
        break

plt.show()

map_center = mapCalcs.get_center(strava_data,12,['long_intrp','lat_intrp'])
corns = mapCalcs.get_corners(zoom,map_center,[map_width,map_height],
in_coord_units='semi',out_coord_units='semi')

print(map_center)
print(corns)
