from formats import formats
import matplotlib.pyplot as plt
import numpy as np
import calcs
import utils
from scipy import interpolate
from calcs import interpolate as calcintrp
from calcs import convert

# for developing in VSCode
import importlib 
importlib.reload(formats)
importlib.reload(calcintrp)
importlib.reload(convert)


# load dateset from folder
read_dir = "new_dataset"
strava_data = formats.read_xlsx(read_dir)

# calculate elapsed time
# elapsed time = timestamp[i] - timestamp[0]
for a_key in strava_data['activities'].keys():
    t_stmp = strava_data['activities'][a_key]['timestamp']
    strava_data['activities'][a_key]['elpsd_time'] = t_stmp - t_stmp[0]

# interpolate data
calcintrp.intrp1d(strava_data,'lat_intrp',['elpsd_time','position_lat'],step_size=1)
calcintrp.intrp1d(strava_data,'long_intrp',['elpsd_time','position_long'],step_size=1)
calcintrp.intrp1d(strava_data,'speed_intrp',['elpsd_time','enhanced_speed'], step_size=1)

# add unit info to data structure
unit_info = {'lat_intrp': 'semicircles',   'long_intrp': 'semicircles',
             'speed_intrp': 'm/s',         'elpsd_time': 'seconds'}
strava_data['units'].update(unit_info)

# write dataset to new directory
new_dir = "Interpolated_Dataset"
formats.write_xlsx(strava_data,new_dir)



print('Done')



# long_min, long_max, lat_min, lat_max = -122.43479368847657, +\
#                                        -122.26313231152345, +\
#                                          47.62217770739337, +\
#                                          47.737752285340434

# long_min_semi,long_max_semi = convert.units('deg_to_semi',np.array([long_min, long_max]))
# lat_min_semi,lat_max_semi = convert.units('deg_to_semi',np.array([lat_min, lat_max]))



# fig, ax = plt.subplots(figsize=(10,10))

# ax.scatter(long,lat,marker='o',s=10)

# ax.scatter(long_new,lat_new,s=2,c='orange')


# img = plt.imread("seattle500x500.png")

# ax.imshow(img, zorder=0,extent=[long_min_semi,long_max_semi,lat_min_semi,lat_max_semi])
# ax.set_aspect(aspect=1.5)
# ax.set_xlim(long_min_semi,long_max_semi) 
# ax.set_ylim(lat_min_semi,lat_max_semi)


# plt.show()