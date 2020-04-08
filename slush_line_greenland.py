# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:29:54 2020

@author: viktorwu02
"""


import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#import gdal

slush_ice = np.zeros((561,301))
slush_ice = slush_ice - 1
 
from netCDF4 import Dataset
file = 'MODIS_2000_2019/2000/Greenland_Reflectivity_2000_5km_C6.nc'
nc = Dataset(file,'r')

slush_list = []

#for i in (1,32,61,92,122,153,183,214,245,275,306,336):
albedos = nc.variables["albedo"][336]
icemask = nc.variables["icemask"]

(rows,cols) = np.shape(albedos)
for r in range(1,rows-1):
    for c in range(1,cols-1):
        temp_window = albedos[r-1:r+2,c-1:c+2]
        mean = np.sum(temp_window)/9
        temp_list = []

        for cell in np.nditer(temp_window, op_flags=['readwrite']):
            variance = (cell - mean)**2
            temp_list.append(variance)
            st_deviation = math.sqrt(sum(temp_list)/9)
                   
        
        if st_deviation >= 0.05 and icemask[r,c] == 1:
                slush_ice[r,c] = 1      
        elif icemask[r,c] != 1 and albedos[r,c] > 0:
                slush_ice[r,c] = 3
        elif icemask[r,c] != 1:
                slush_ice[r,c] = -1           
        else:        
                slush_ice[r,c] = 2

#matplotlib plots
                              
    slush_ice = np.flipud(slush_ice)

    #slush_list.append(slush_ice)

from matplotlib.colors import from_levels_and_colors

lats = nc.variables['lat'][:]
lats = np.flipud(lats)


lons = nc.variables['lon'][:]
lons = np.flipud(lons)


cmap, norm = from_levels_and_colors([-1,1,2,3,4],['white','orangered','azure','silver'])

#plot one

fig = plt.figure(figsize=(8, 6))
m = Basemap(projection='lcc', resolution='l',
            width=2E6, height=3E6, lat_0=72, lon_0=-37,)
mplot = m.pcolormesh(lons, lats, slush_ice,latlon=True, cmap=cmap, norm=norm)
mplot = m.drawparallels(np.arange(-80.,81.,10.),labels=[True,False,True,False])
mplot = m.drawmeridians(np.arange(-180.,181.,20.),labels=[False,False,False,True])
plt.clim(-1, 4)
plt.title('Slush-line test')
plt.colorbar(label='legend'); 

#plot 4x3

#fig, axes = plt.subplots(figsize=(12,9),nrows=3, ncols=4)
#for ax in axes.flat:
#    map_ax = Basemap(ax=ax, projection='lcc', resolution='l',
#            width=2E6, height=3E6, lat_0=72, lon_0=-37)
#    for i in slush_list:
#        for ax in axes.flat:
#            ax = map_ax.pcolormesh(lons, lats, i,latlon=True, cmap=cmap, norm=norm)
#    map_ax.drawparallels(np.arange(-80.,81.,10.),labels=[False,True,False,True])
#    axes[0, 0].set_title("January")
#    axes[0, 1].set_title("February")
#    axes[0, 2].set_title("March")
#    axes[0, 3].set_title("April")
#    axes[1, 0].set_title("May")
#    axes[1, 1].set_title("June")
#    axes[1, 2].set_title("July")
#    axes[1, 3].set_title("August")
#    axes[2, 0].set_title("September")
#    axes[2, 1].set_title("October")
#    axes[2, 2].set_title("November")
#    axes[2, 3].set_title("December")
#plt.show()


# create output

#header = "ncols {}\n".format(slush_ice.shape[1])
#header += "nrows {}\n".format(slush_ice.shape[0])
#header += "xllcorner -440510.18862\n"
#header += "yllcorner -3467275.427575\n"
#header += "cellsize 5000\n"
#header += "NODATA_value -9999"

#np.savetxt("slush2012"+"_thresh8_5_wtr"+".asc",slush_ice, header=header, fmt="%1.2f", comments='')

## KAN_U Station 

#fig = plt.figure(figsize=(8, 6))
#m = Basemap(projection='lcc', resolution='l',
#            width=0.15E6, height=0.35E6, lat_0=67, lon_0=-47,)
#mplot = m.pcolormesh(lons, lats, slush_ice,latlon=True, cmap=cmap, norm=norm)
#mplot = m.drawparallels(np.arange(-80.,81.,10.),labels=[True,False,True,False])
#mplot = m.drawmeridians(np.arange(-180.,181.,20.),labels=[False,False,False,True])
#plt.clim(-1, 4)
#plt.title('KAN_U test')
#plt.colorbar(label='legend');
#lat, lon = 67.0003, -47.0243
#x, y = m(lon, lat)
#plt.scatter(x, y, marker = 'o', color='green')


#width=0.7E6, height=1E6, lat_0=67, lon_0=-45,)



##########################


   