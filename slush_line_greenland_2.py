# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:29:54 2020

@author: viktorwu02
"""


import numpy as np
import math
#import gdal

slush_ice = np.zeros((561,301))
slush_ice = slush_ice - 1
 
from netCDF4 import Dataset
file = 'MODIS_2000_2019/2014/Greenland_Reflectivity_2014_5km_C6.nc'
nc = Dataset(file,'r')


for i in range(0,366):
    albedos = nc.variables["albedo"][i]
    icemask = nc.variables["icemask"]

    (rows,cols) = np.shape(albedos)
    for r in range(2,rows-2):
        for c in range(2,cols-2):
            temp_window = albedos[r-2:r+3,c-2:c+3]
            mean = np.sum(temp_window)/25
            temp_list = []

            for cell in np.nditer(temp_window, op_flags=['readwrite']):
                variance = (cell - mean)**2
                temp_list.append(variance)
                st_deviation = math.sqrt(sum(temp_list)/25)
        
           # print(st_deviation)
        
                if st_deviation >= 0.0125 and icemask[r,c] == 1:
                        slush_ice[r,c] = 1      
                elif icemask[r,c] != 1:
                        slush_ice[r,c] = -1            
                else:        
                        slush_ice[r,c] = 2

# create output from slush_ice

                slush_ice = np.flipud(slush_ice)
                header = "ncols {}\n".format(slush_ice.shape[1])
                header += "nrows {}\n".format(slush_ice.shape[0])
                header += "xllcorner -440510.18862\n"
                header += "yllcorner -3467275.427575\n"
                header += "cellsize 5000\n"
                header += "NODATA_value -9999"

                np.savetxt("slush2014"+"_str(i)"+".asc",slush_ice, header=header, fmt="%1.2f", comments='')


#or

#driver = gdal.GetDriverByName('Gtiff')
#dataset = driver.Create('slush_line.tif', 301, 561, 1, gdal.GDT_UInt16)
#dataset.GetRasterBand(1).WriteArray(slush_ice)
#dataset = None # "Closing" the driver


##########################


   