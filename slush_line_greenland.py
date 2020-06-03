# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:29:54 2020

@author: viktorwu02
"""


import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point
from shapely.geometry import Polygon

 
from netCDF4 import Dataset

for year in range(2000,2020):

    file = 'MODIS_2000_2019/' + year + '/Greenland_Reflectivity_' + year + '_5km_C6.nc'
#file = 'MODIS_2000_2019/2012/Greenland_Reflectivity_2012_5km_C6.nc'
    nc = Dataset(file,'r')
        
### To calculate the cumulative slush-days
        
    for day in range(1,366):
    
        albedos = nc.variables["albedo"][day]
        icemask = nc.variables["icemask"]
        dem = nc.variables["dem"]
        lats = nc.variables['lat'][:]
        lons = nc.variables['lon'][:]
        mod_lons = lons + 360
        cumulative_slush = np.zeros((561,301))
    
        (rows,cols) = np.shape(dem)
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
                        cumulative_slush[r,c] += 1
                
### To classify one image
                    
file = 'MODIS_2000_2019/2012/Greenland_Reflectivity_2012_5km_C6.nc' 
nc = Dataset(file,'r')
                 
albedos = nc.variables["albedo"][day]
icemask = nc.variables["icemask"]
dem = nc.variables["dem"]
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:]
mod_lons = lons + 360
slush_ice = np.zeros((561,301))
    
(rows,cols) = np.shape(dem)
for r in range(1,rows-1):
    for c in range(1,cols-1):
        temp_window = albedos[r-1:r+2,c-1:c+2]
        mean = np.sum(temp_window)/9
        temp_list = []
        
        for cell in np.nditer(temp_window, op_flags=['readwrite']):
            variance = (cell - mean)**2
            temp_list.append(variance)
            st_deviation = math.sqrt(sum(temp_list)/9)

            if st_deviation >= 0.05 and icemask[r,c] == 1 and cumulative_slush[r,c] < 2800:                
                        slush_ice[r,c] = 1
            elif icemask[r,c] != 1 and albedos[r,c] > 0:
                        slush_ice[r,c] = 3
            elif icemask[r,c] != 1:
                        slush_ice[r,c] = -1           
            else:        
                        slush_ice[r,c] = 2



### To count pixels in drainage systems   

#if st_deviation >= 0.05 and icemask[r,c] == 1 and slush_hotspot[r,c] < 2800 and Polygon(polyname).contains(Point(lats[r,c],mod_lons[r,c])):      
                    
#pixlist21.append(len(slush_list))
#topelev21.append(np.percentile(slush_list,90))



    
         
                 
#slush_ice = np.flipud(slush_ice)

        #slush_list.append(slush_ice)





#plot one

#from matplotlib.colors import from_levels_and_colors
#cmap, norm = from_levels_and_colors([-1,1,2,3,4],['white','orangered','azure','silver'])
#fig = plt.figure(figsize=(8, 6))
#m = Basemap(projection='lcc', resolution='l',
#            width=2E6, height=3E6, lat_0=72, lon_0=-37,)
#mplot = m.pcolormesh(lons, lats, slush_ice,latlon=True, cmap=cmap, norm=norm)
#mplot = m.drawparallels(np.arange(-80.,81.,10.),labels=[True,False,True,False])
#mplot = m.drawmeridians(np.arange(-180.,181.,20.),labels=[False,False,False,True])
#plt.clim(-1, 4)
#plt.title('Slush on GrIS')
#plt.colorbar; 



     
# To create output

#header = "ncols {}\n".format(slush_ice.shape[1])
#header += "nrows {}\n".format(slush_ice.shape[0])
#header += "xllcorner -440510.18862\n"
#header += "yllcorner -3467275.427575\n"
#header += "cellsize 5000\n"
#header += "NODATA_value -9999"

#np.savetxt("slush2019"+"_thresh8_5_wtr"+".asc",slush_ice, header=header, fmt="%1.2f", comments='')






##### To load polygons
    
#with open('GrnDrainageSystems_Ekholm.txt', 'r') as f:

 #   data = f.readlines() # Reading all data
    
    # Removing header
 #  idx = 0
 #   while not 'END OF HEADER' in data[idx]:
 #       print(data[idx]) # If you want to print the header
 #       idx += 1
    
    # Extracting the first point of the first polygon
    # Needs to start at idx+1 since not incrementing after found end of header
 #   tempLine = data[idx+1] # Current coordinate
 #  print(tempLine.split(' '))
 #   tempPoint = tempLine.strip().split(' ') # Removing leading (and ending) spaces and splitting
    # indices that gives:
    # code, latitude, longitude:
    # [0],[6],[11]
        
    #Extracting the point of each polygon
  #  tempPolyID = float(tempPoint[0])
   #
  # polyList.append((float(tempPoint[6]), float(tempPoint[11])))
    # tempPolyList is a list with polygon ID followed by a series of tuples with lat,lon coordinates for that polygon
                
    
    
    
    # Start looping over the data.
  #  for i in range(idx+2, len(data)):
   #     tempLine = data[i] # Current coordinate
    #   tempPoint = tempLine.strip().split(' ') # Removing leading (and ending) spaces and splitting
        
     #   if float(tempPoint[0]) == tempPolyID: # Not recommended to use == for float....
            # New point of current polygon               
      #      polyList.append((float(tempPoint[6]), float(tempPoint[11])))
     #   else:
            # New polygon
       #     tempPolyID = float(tempPoint[0])
        #    polyList.append(tempPolyID)
         #   polyList.append((float(tempPoint[6]), float(tempPoint[11])))



##########################


#fig = plt.figure(figsize=(8, 6))
#cmap = plt.get_cmap('rainbow')
#cmap.set_under('white') 
#m = Basemap(projection='lcc', resolution='l',
#            width=2E6, height=3E6, lat_0=72, lon_0=-37,)
#mplot = m.pcolormesh(lons, lats, slush_hotspot, vmin= 0.5, cmap=cmap, latlon=True)
#mplot = m.drawparallels(np.arange(-80.,81.,10.),labels=[True,False,True,False])
#mplot = m.drawmeridians(np.arange(-180.,181.,20.),labels=[False,False,False,True])
#mplot = m.drawcoastlines()
#plt.title('Cumulative slush-days')
#plt.colorbar;
   