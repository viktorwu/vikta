# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#This script is used to calculate Half-Recovery Time (HRT) for burned areas of different land-cover class
#HRT is defined as the amount of days it takes for the difference in NDVI between burned area and a unburned reference area to be reduced by 50% from the time of peak disturbance
#The script produces a DataFrame with calculated HRT for each fire in the dataset and includes Fire ID, date of fire, lat/lon, total area and HRT for each individual land-cover class

import pandas as pd
import numpy as np
import math
import datetime
import seaborn as sns
#import csv
from pathlib import Path
from scipy import stats
import matplotlib.pyplot as plt
from statannot import add_stat_annotation

#Create header for output from GEE
top_header = ['FIRE_ID','date','lat','lon','total area','lc_1','lc_2','lc_3','lc_4','lc_5','lc_6','lc_7','lc_8','lc_9','lc_10','lc_11','lc_12','lc_13']
hrt_df = pd.DataFrame(top_header)
hrt_df = hrt_df.transpose()

#Loop over all fires in the dataset
no_fires = 294
for i in range(1,(no_fires+1)):
    file = 'P:/Desktop/viktor_fires/dNDVI_Fire_' + str(i) + '.csv'
#file = 'P:/Desktop/viktor_fires/dNDVI_Fire_10.csv'    
    my_csv = Path(file)
    df = pd.read_csv(my_csv.resolve(), sep=',')

    # IF LOOPING AND ADDING AS LIST TO DATAFRAME; ROWS BELOW NEED TO BE INCLUDED IN LOOP
    
    lc_1 = []
    lc_2 = []
    lc_3 = []
    lc_4 = []
    lc_5 = []
    lc_6 = []
    lc_7 = []
    lc_8 = []
    lc_9 = []
    lc_10 = []
    lc_11 = []
    lc_12 = []
    lc_13 = []
#Create variable for Fire_n after import
#Fire_1 = dNDVI_Fire_1csv[1:len(dNDVI_Fire_1csv),1:4]
#dNDVI = NDVI_only.apply(lambda s: [float(x.strip(' []')) for x in s.split(',')])

    Fire = df

    df["prop"] = df["prop"].str.replace("\[|\]|\'", "").str.split(",")
    df.join(pd.DataFrame(df["prop"].values.tolist()).add_prefix('lc'))

#Create array for individual fire
    fire_array = pd.DataFrame(df['prop'].tolist())


    header = fire_array[0:1][0:len(fire_array[0:1])]
    header = header.to_numpy()
    header = header.astype('str')
    header = header.tolist()
    header = header[0] 

    hdr = []
# Output from GEE produces spaces in header
    for i in header:
        i = i.strip()
        hdr.append(i)

#Get only NDVI timeseries from fire data
    NDVI_only = fire_array[2:len(Fire)]

#Format date column        
    NDVI_only[0] = pd.to_numeric(NDVI_only[0], downcast="float")
    NDVI_only[0] = pd.to_datetime(NDVI_only[0], unit='ms')
    NDVI_only[0] = NDVI_only[0] + pd.to_timedelta(3,unit='m')
    NDVI_only[0] = NDVI_only[0].dt.date    

#Find start of recovery (peak disturbance)        
    s = fire_array[1][1]
    s = float(s)
    s = s/1000
    recovery_start = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
    recovery_start = datetime.datetime.strptime(recovery_start,'%Y-%m-%d %H:%M:%S')
    recovery_start = recovery_start.date()

#Find NDVI value at start of recovery    
    start = NDVI_only[NDVI_only[0]==recovery_start]
    start = start.to_numpy()
        
    ndvi_start = start[:,1:]
    ndvi_start = ndvi_start.astype(np.float)
    
    dNDVI = NDVI_only.to_numpy()
    start_index = np.where(dNDVI == recovery_start)[0][0]

#Cut NDVI timeseries to start at peak disturbance        
    cut_dNDVI = dNDVI[start_index:,:]

#Calculate HRT for each land cover class
    for column, i, name in zip(cut_dNDVI[:,1:].T,ndvi_start.T,range(5,len(hdr))):
        list = column
        list = column.astype(np.float)
        days = next(x[0] for x in enumerate(list) if x[1] > (i/2))
        lc_recovery = globals()[hdr[name]]
        lc_recovery.append(days*8)
 
 #Add HRT for each land cover class to DatFrame   
    comb_list = [lc_1,lc_2,lc_3,lc_4,lc_5,lc_6,lc_7,lc_8,lc_9,lc_10,lc_11,lc_12,lc_13]
    flat_list = [name for sublist in comb_list for name in (sublist or [np.nan])]
    fire_inf = [int(fire_array[0][1]),recovery_start,float(fire_array[2][1]),float(fire_array[3][1]),int(fire_array[4][1])]
    fire_inf.extend(flat_list) 
    hrt_df.loc[len(hrt_df)] = fire_inf
