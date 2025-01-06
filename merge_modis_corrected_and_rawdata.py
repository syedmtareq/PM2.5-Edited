#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 15:09:50 2018

@author: mbarik
"""
import pandas as pd

import os

def process(QC, year, DOY, rawdata_output_path):
    
    
    if (os.path.getsize(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+DOY+'.txt') > 0)==True:
        MODIS_bias_corrected_path=r'MODIS_rawdata_DOY{}.txt'.format(DOY)
        
        modDF=pd.read_csv(MODIS_bias_corrected_path, sep="\t", header=None, engine='python')
        modDF[3]=0
        #print (modDF)
        data_final_path='MODIS_bias_corrected_and_rawdata.txt'
        data_final_path_DOY='./rawdata/MODIS_bias_corrected_and_rawdata_{}.txt'.format(DOY)
        #data_final_path='rawdatalog_IDW_final.txt'
        
        if QC=='yes':
            AQS_data_path=r'AQS_rawdata_QC_{}_DOY{}.txt'.format(year,DOY)
        else:
            AQS_data_path=r'AQS_rawdata_noQC_{}_DOY{}.txt'.format(year,DOY)
        AQSDF=pd.read_csv(AQS_data_path, sep="\t", header=None, engine='python')
        AQSDF[3]=1
        newDF=pd.concat([modDF,AQSDF])
        newDF=newDF.reset_index(drop=True)
        
        newDF.to_csv(data_final_path , encoding='utf-8', sep='\t', index=True, header=False) 
        
        newDF.to_csv(data_final_path_DOY , encoding='utf-8', sep='\t', index=True, header=False) 
    else:
        data_final_path='MODIS_bias_corrected_and_rawdata.txt'
        data_final_path_DOY='./rawdata/MODIS_bias_corrected_and_rawdata_{}.txt'.format(DOY)
        
        if QC=='yes':
            AQS_data_path=r'AQS_rawdata_QC_{}_DOY{}.txt'.format(year,DOY)
        else:
            AQS_data_path=r'AQS_rawdata_noQC_{}_DOY{}.txt'.format(year,DOY)
        AQSDF=pd.read_csv(AQS_data_path, sep="\t", header=None, engine='python')
        AQSDF[3]=1
        

        
        AQSDF.to_csv(data_final_path , encoding='utf-8', sep='\t', index=True, header=False) 
        
        AQSDF.to_csv(data_final_path_DOY , encoding='utf-8', sep='\t', index=True, header=False) 
        
    
