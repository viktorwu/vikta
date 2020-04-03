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
file = 'MODIS_2000_2019/2014/Greenland_Reflectivity_2014_5km_C6.nc'
nc = Dataset(file,'r')


#for i in range(0,366):
albedos = nc.variables["albedo"][1]
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
                   
        
        if st_deviation >= 0.0125 and icemask[r,c] == 1:
                slush_ice[r,c] = 1      
        elif icemask[r,c] != 1 and albedos[r,c] > 0:
                slush_ice[r,c] = 3 
        elif icemask[r,c] != 1:
                slush_ice[r,c] = -1           
        else:        
                slush_ice[r,c] = 2

#matplotlib plots
                              
slush_ice = np.flipud(slush_ice)

from matplotlib.colors import from_levels_and_colors

lat = nc.variables['lat'][:]
lat = np.flipud(lat)


lon = nc.variables['lon'][:]
lon = np.flipud(lon)


cmap, norm = from_levels_and_colors([-1,1,2,3,4],['white','orangered','azure','silver'])

fig = plt.figure(figsize=(8, 6))
m = Basemap(projection='lcc', resolution='l',
            width=2E6, height=3E6, lat_0=72, lon_0=-37,)
mplot = m.pcolormesh(lon, lat, slush_ice,latlon=True, cmap=cmap, norm=norm)
mplot = m.drawparallels(np.arange(-80.,81.,10.),labels=[True,False,True,False])
mplot = m.drawmeridians(np.arange(-180.,181.,20.),labels=[False,False,False,True])
plt.clim(-1, 4)
plt.title('Slush-line test')
plt.colorbar(label='legend'); 




# create output

#header = "ncols {}\n".format(slush_ice.shape[1])
#header += "nrows {}\n".format(slush_ice.shape[0])
#header += "xllcorner -440510.18862\n"
#header += "yllcorner -3467275.427575\n"
#header += "cellsize 5000\n"
#header += "NODATA_value -9999"

#np.savetxt("slush2014"+"_3by3_1"+".asc",slush_ice, header=header, fmt="%1.2f", comments='')


#"slush2014"+"_str(i)"+".asc"

#driver = gdal.GetDriverByName('Gtiff')
#dataset = driver.Create('slush_line.tif', 301, 561, 1, gdal.GDT_UInt16)
#dataset.GetRasterBand(1).WriteArray(slush_ice)
#dataset = None # "Closing" the driver


##########################


   