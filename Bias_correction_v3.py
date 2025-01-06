#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mbarik
"""

import os 
from pandas import DataFrame
import pandas as pd
import numpy as np

def process(rawdata_output_path, pixelsfile_path, DOY, w):
    print('begining of MODIS data bias correction subroutine')
    print('-----------------------------------')
    ## opening file for reading data ###
    MODIS_IDW_path=r'MODIS_IDW.txt'
    AQS_IDW_path=r'AQS_IDW.txt'
    MODIS_data_path=r'MODIS_rawdata_DOY'+DOY+'.txt' #Day 4


    MODIS_IDW=pd.read_csv(MODIS_IDW_path,header=None, sep='\t')
    AQS_IDW=pd.read_csv(AQS_IDW_path,header=None, sep='\t')
    pixels=pd.read_csv(pixelsfile_path,header=None, sep=',')
    MODIS_data=pd.read_csv(MODIS_data_path,header=None, sep='\t')
    
    
    ######## files for writing data ##############
    bias_file_path=r'bias_.txt'
    MODIS_bias_corrected_path=r'MODIS_Bias_Removed.txt'
    MODIS_bias_corrected_path_with_header=rawdata_output_path+'//' +'MODIS_Bias_Removed_with_header.txt'
    
    bias_file_path_DOY=r'./rawdata/bias_{}.txt'.format(DOY)
    MODIS_bias_corrected_path_DOY=r'./rawdata/MODIS_Bias_Removed_{}.txt'.format(DOY)

    
    
    
    
    ##### Determining bias ########################
    
    bias=MODIS_IDW-AQS_IDW
    
    bias=pd.concat([pixels.iloc[:,0:2], bias], axis=1)
    
    bias.to_csv(bias_file_path, encoding='utf-8', sep='\t', index=False, mode='w', header=False)
    bias.to_csv(bias_file_path_DOY, encoding='utf-8', sep='\t', index=False, mode='w', header=False)
    
    bias.columns=['lon','lat','pm']
    
    MODIS_data.columns=['lon','lat','pm']
    
    for l in range(MODIS_data.shape[0]):
    
        lon=MODIS_data.iloc[l,0]
        lat=MODIS_data.iloc[l,1]
        pm=MODIS_data.iloc[l,2]
        #print(lon,lat)
    
        
        selected=bias.iloc[np.intersect1d(np.where(abs(lon-bias.iloc[:,0])<=float(0.03)), np.where(abs(lat-bias.iloc[:,1])<=float(0.03)))]
        #print(selected.mean(axis=0)['pm'])
        MODIS_data.iloc[l,2]=pm-selected.mean(axis=0)['pm'] # correecting bais and replacing the raw value with bias corrected value  
    
    MODIS_data.to_csv(MODIS_bias_corrected_path, encoding='utf-8', sep='\t', index=False, mode='w', header=False)
    MODIS_data.to_csv(MODIS_bias_corrected_path_DOY, encoding='utf-8', sep='\t', index=False, mode='w', header=False)
    
    #writing again with using a common file name 
    if os.path.exists(MODIS_bias_corrected_path_with_header):
                os.remove(MODIS_bias_corrected_path_with_header) # deleting an already existing file from previous timestep, since appending will be done 
    if not os.path.exists(MODIS_bias_corrected_path_with_header): #header only for the first loop 
              with open(MODIS_bias_corrected_path_with_header,'w') as f:
                  f.write(w)
                  f.write('\n')
                  f.write(' ')
                  f.write(str(MODIS_data.shape[0]))
                  f.write('\n')
    MODIS_data.to_csv(MODIS_bias_corrected_path_with_header, encoding='utf-8', sep='\t', index=False, mode='a', header=False)



                









