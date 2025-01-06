#!/usr/bin/env python3
# This code do the mosaicing and MDOIS Pm2.5 estiamtion from MODIS AOD
# Final output is mosaiced MODIS Pm2.5 
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:15:07 2017

@author: barik
"""

from osgeo import gdal
import glob
import os
import numpy as np
import pandas as pd



def mosaic(day, band, year, slp, intr,slp1, intr1,slp2, intr2,slp3, intr3, latmin, latmax, lonmin, lonmax, xcells, ycells, MODIS_data_path, rawdata_output_path, w ):

    DT_string = 'Corrected_Optical_Depth_Land' 
    lon_string = '0' #SDS
    lat_string = '1' #SDS

    if band == '0.47': bs = 0
    elif band == '0.55': bs = 1 
    elif band == '0.66': bs = 2
    else: print ('Invalid band')
    
   
    
    files = glob.glob(MODIS_data_path+'*.hdf')
    

    location = {'Latitude' : [], 'Longitude' : [], 'DT_AOD' : []} 
    day = str('%0.3d' % day)
    print (day)
    
    count=0
    for i in files:
     
     file_name=os.path.basename(i)
     
     dayfname = file_name[14:17]         #determining the day of each file
     #daytimefname = file_name[14:22]         #determining the day of each file
     yeardayfnametime = file_name[10:14] #finding the year, date, and time  
     
     if file_name[-4:] == '.hdf'and file_name[14:17]==day and yeardayfnametime==year: #
      count=count+1   
      print(os.path.basename(i))
      location = {'Latitude' : [], 'Longitude' : [], 'DT_AOD' : []} 
      lon_key = 'HDF4_SDS:UNKNOWN:"{}":{}'.format(i, lon_string)
      lat_key = 'HDF4_SDS:UNKNOWN:"{}":{}'.format(i, lat_string)
      DT_key  = 'HDF4_EOS:EOS_SWATH:"{}":mod04:{}'.format(i, DT_string) #EOS
      #saving the data as arrays for easier interpretation
      longitude = gdal.Open(lon_key).ReadAsArray()
      latitude = gdal.Open(lat_key).ReadAsArray()
      DT_AOD = gdal.Open(DT_key).ReadAsArray()
                
      DT_AOD = DT_AOD * 0.001 #scale factor provided by HDF view app
      
      
      lon1d=longitude.flatten()
      lat1d=latitude.flatten()
      DT_AOD1d=DT_AOD[bs,:,:].flatten()
      
      
      dataset = pd.DataFrame({ 'lon':lon1d , 'lat':lat1d, 'AOD':DT_AOD1d })
      
      dataset  = dataset [['lon','lat','AOD']] 
      

      
      conditions = (dataset['lon']>lonmin, dataset['lon']<lonmax, dataset['lat']>latmin, dataset['lat']<latmax, dataset['AOD']>=-0.1)  
      indices = np.where(np.logical_and.reduce(conditions))
      subsetAOD = dataset['AOD'].iloc[indices]
      subsetlon1d = dataset['lon'].iloc[indices]
      subsetlat1d = dataset['lat'].iloc[indices]
      
      subsetPM=subsetAOD*slp+intr
      
      subsetPM=np.where(np.logical_and(subsetlat1d>38, subsetlat1d<42), (subsetAOD*slp1+intr1), subsetPM)
      subsetPM=np.where(np.logical_and(subsetlat1d>35, subsetlat1d<38), (subsetAOD*slp2+intr2), subsetPM)
      subsetPM=np.where(np.logical_and(subsetlat1d>32, subsetlat1d<35), (subsetAOD*slp3+intr3), subsetPM)
      subsetPM = pd.DataFrame({ 'PM':subsetPM })
      subsetlon1d = pd.DataFrame({ 'lon':subsetlon1d })
      subsetlat1d = pd.DataFrame({ 'lat':subsetlat1d})
      subsetlon1d=subsetlon1d.reset_index(drop=True)
      subsetlat1d=subsetlat1d.reset_index(drop=True)
      #print(subsetlon1d)
        
      #mergedDF=pd.concat([subsetlon1d, subsetlat1d , subsetAOD*slp+intr], axis=1) 
      mergedDF=pd.concat([subsetlon1d, subsetlat1d , subsetPM], axis=1) 
      #mergedDF.to_csv(os.path.dirname(i)+ '/' + 'MODIS_rawdata_DOY'+daytimefname+'_0831_df.txt' , encoding='utf-8', sep='\t', index=False, header=False)
      
      if os.path.exists(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+dayfname+'.txt') and count==1:
          os.remove(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+dayfname+'.txt')
      
      if not os.path.isfile(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+dayfname+'.txt'):
          mergedDF.to_csv(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+dayfname+'.txt', header=False,encoding='utf-8', sep='\t', index=False)
      else: # else it exists so append without writing the header
          mergedDF.to_csv(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+dayfname+'.txt', mode='a', encoding='utf-8', sep='\t', index=False,header=False)
      
      #mergedDF.to_csv(os.path.dirname(i)+ '/' + 'MODIS_rawdata_DOY'+dayfname+'_0831_df.txt' ,'a' ,encoding='utf-8', sep='\t', index=False, header=False) 
    
    
    if os.path.exists(rawdata_output_path+ '/' + 'MODIS_rawdata.txt'):
          os.remove(rawdata_output_path+ '/' + 'MODIS_rawdata.txt')
    if not (os.path.isfile(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+day+'.txt')):
        open(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+day+'.txt', 'a').close()
    #loading merged mosaic data 
    if (os.path.getsize(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+day+'.txt') > 0)==True:
        
        dataDF=pd.read_csv(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+day+'.txt', sep="\t", header=None) 

        #writing merged MODIS rawdata with header  
        with open(rawdata_output_path+ '/' + 'MODIS_rawdata.txt', 'w') as f:
                                  f.write(w)
                                  f.write('\n')
                                  f.write('  ')
                                  f.write(str(len(dataDF.index)))
                                  f.write('\n')
        dataDF.to_csv(rawdata_output_path+ '/' +'MODIS_rawdata.txt',mode='a', header=False, sep='\t', index=False)
    
    
    
#    ##Average MODIS data over the selected region 
#    if not dataDF.empty:
#         modis_average_over_region=dataDF[2].mean()
#         if os.path.exists(rawdata_output_path+ '/' + 'obsmean16_MODIS.txt'):
#                            os.remove(rawdata_output_path+ '/' + 'obsmean16_MODIS.txt') # deleting an already existing file from previous timestep, since appending will be done 
#         if not os.path.exists(rawdata_output_path+ '/' + 'obsmean16_MODIS.txt'): #header only for the first loop 
#                          with open(rawdata_output_path+ '/' + 'obsmean16_MODIS.txt', 'w') as f:
#                              f.write(w)
#                              f.write('\n')
#                              f.write('  ')
#                              f.write(str(xcells*ycells))
#                              f.write('\n')
#                
#         for x in range(xcells):
#           for y in range(ycells):
#             #print( latmin+((latmax-latmin)/(ycells-1))*y ,',', lonmin+((lonmin-lonmin)/(xcells-1))*x)
#             with open(rawdata_output_path+ '/' + 'obsmean16_MODIS.txt', 'a') as f:
#                              f.write('     ')
#                              f.write(str('%0.6f' %(lonmin+((lonmax-lonmin)/(xcells-1))*x)))
#                              f.write('\t')
#                              f.write(str('%0.6f' %(latmin+((latmax-latmin)/(ycells-1))*y)))
#                              f.write('\t')
#                              f.write(str('%0.6f' %(modis_average_over_region)))
#                              f.write('\n')


      
