#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: mbarik
"""
import pandas as pd
import numpy as np
import time

def frac(lat1,long1, inDF):
            #start=time.time() 
            selected=inDF.iloc[np.intersect1d(np.where(abs(long1-inDF.lon.values)<=float(0.03)), np.where(abs(lat1-inDF.lat.values)<=float(0.03)))]
            checkselect=selected.iloc[np.where(selected.flag.values==1)] #check for AQS data in the cell 
            #checkselect=selected.loc[selected['flag']==1] #check for AQS data in the cell 
            #print(checkselect)
            #end1=time.time()
            #print("after selection %s" %(end1-start))
            if checkselect.empty==False: #if any AQS data in the cell, take only the mean of AQS data  
                wpm=checkselect.mean(axis=0)['PMb']
                #end2=time.time()
                #print("after AQS on cell check %s" %(end2-start))
            else:
                inDF['dist']=(lat1-inDF.lat.values)**2+ (long1-inDF.lon.values)**2
                inDF50=inDF[(inDF['dist'])<0.2] #seelct all the points within 20 Km radious
                if inDF50.shape[0]<12: # check if at least 12 modis points within 20 KM then apply IDW on all data  
                    #print('No Data with 50 km')
                    inDF1=inDF[inDF.flag==1]
                    inDF1.columns = ['ID', 'lon','lat','PMb','flag','dist']
                    #inDF2=sorted_12pts.iloc[np.where(sorted_12pts.flag.values==0)] #select all MODIS data 
                    inDF2=inDF[inDF.flag==0]
                    inDF2.columns = ['ID', 'lon','lat','PMb','flag','dist']   
                    #end4=time.time()
                    #print("after ind1 and ind2 %s" %(end4-start))
                    sumD=(1/((lat1-inDF1.lat.values)**2+ (long1-inDF1.lon.values)**2)).sum()*0.9+ (1/((lat1-inDF2.lat.values)**2+ (long1-inDF2.lon.values)**2)).sum()*0.1
                    sumN=(inDF1.PMb.values/((lat1-inDF1.lat.values)**2+ (long1-inDF1.lon.values)**2)).sum()*0.9+ (inDF2.PMb.values/((lat1-inDF2.lat.values)**2+ (long1-inDF2.lon.values)**2)).sum()*0.1
                    wpm=sumN/sumD
                #end6=time.time()
                #print("after dist %s" %(end6-start))
                elif inDF50.shape[0]>=12: #checking if there are atlest 12 MODIS points available 
                    sorted_12pts=inDF50.sort_values(['dist'], ascending=True)[0:12].reset_index(drop=True) #seelct only 12 points 
                    inDF1=sorted_12pts[sorted_12pts.flag==1]
                    inDF1.columns = ['ID', 'lon','lat','PMb','flag','dist']
                    #inDF2=sorted_12pts.iloc[np.where(sorted_12pts.flag.values==0)] #select all MODIS data 
                    inDF2=sorted_12pts[sorted_12pts.flag==0]
                    inDF2.columns = ['ID', 'lon','lat','PMb','flag','dist']   
                    #end4=time.time()
                    #print("after ind1 and ind2 %s" %(end4-start))
                    sumD=(1/((lat1-inDF1.lat.values)**2+ (long1-inDF1.lon.values)**2)).sum()*0.9+ (1/((lat1-inDF2.lat.values)**2+ (long1-inDF2.lon.values)**2)).sum()*0.1
                    sumN=(inDF1.PMb.values/((lat1-inDF1.lat.values)**2+ (long1-inDF1.lon.values)**2)).sum()*0.9+ (inDF2.PMb.values/((lat1-inDF2.lat.values)**2+ (long1-inDF2.lon.values)**2)).sum()*0.1
                    wpm=sumN/sumD
            return(wpm)
       
def IDW(inDF, outDF):       
       outDF['pm']=outDF.apply(
        lambda row: frac(row['lat'], row['lon'], inDF), 
        axis=1)
       return (outDF)

    
def process(QC, cellsizex,cellsizey, ix, iy, latmin, lonmin, DOY, pixelsfile_path):
    print('begining of IDW surfacing subroutine')
    print('-----------------------------------')
    
    pixels=pd.read_csv(pixelsfile_path,header=None, sep=',')
    nrows=int(1935)
    ncols=int(840)
    
    
    
    MODIS_bias_corrected_path=r'./MODIS_Bias_Removed_copy.txt' #### Activated
    
    #IDW_cells_path=r'./IDW_surface_cells_coordinates.txt'
    
    if QC=='yes':
        IDW_final_path=r'./output/Final_Results_IDW_QC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
        IDW_final_alldays_path=r'./output/Final_Results_IDW_QC_Surface_all.txt'.format(DOY)
    else:
        IDW_final_path=r'./output/Final_Results_IDW_noQC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
        IDW_final_alldays_path=r'./output/Final_Results_IDW_noQC_Surface_all.txt'.format(DOY)
    
    IDW_rawdata_path=r'./MODIS_bias_corrected_and_rawdata.txt'
    
    rawDF=pd.read_csv(IDW_rawdata_path, sep='\t', header=None)
    
    rawDF.columns = ['ID', 'lon','lat','PMb','flag']
    
    
    #dataDF=pd.read_csv(MODIS_bias_corrected_path, sep='       ', header=None, skiprows=2)
    
    IDWres = pd.DataFrame( columns=['lon','lat','pm'], index=range(ncols*nrows))
    
    start=time.time()            
    IDWres['lon']=pixels[0]
    IDWres['lat']=pixels[1]
    #print (IDWres)
    
    IDWres=IDW(rawDF,IDWres)
    end=time.time()
    print("%s" %(end-start))
    
#    count=0
#    for r in range(1,nrows+1):
#        for c in range(1,ncols+1):
#            #print(count)
#            if count%10000==0:
#               print(count)
#            
#            ilat=latmin+(r-1)*cellsizex
#            ilon=lonmin+(c-1)*cellsizey
#            
#            IDWres.loc[count].lat=latmin+(r-1)*cellsizex
#            IDWres.loc[count].lon=lonmin+(c-1)*cellsizey
#            
#            selected=rawDF.iloc[np.intersect1d(np.where(abs(ilon-rawDF.lon)<=float(0.03)), np.where(abs(ilat-rawDF.lat)<=float(0.03)))]
#            checkselect=selected.iloc[np.where(selected.flag==1)] #check for AQS data in the cell 
#            
#            if checkselect.empty==False: #if any AQS data in the cell, take only the mean of AQS data  
#                IDWres.loc[count].pm=checkselect.mean(axis=0)['PMb']
#            else:
#                rawDF['dist']=(ilat-rawDF.lat)**2+ (ilon-rawDF.lon)**2
#                
#                sorted_12pts=rawDF.sort_values(['dist'], ascending=True)[0:12].reset_index(drop=True)
#                #print(sorted_12pts)
#                AQSDF=sorted_12pts.iloc[np.where(sorted_12pts.flag==1)] #select all AQS data 
#                AQSDF.columns = ['ID', 'lon','lat','PMb','flag','dist']
#                MODDF=sorted_12pts.iloc[np.where(sorted_12pts.flag==0)] #select all MODIS data 
#                MODDF.columns = ['ID', 'lon','lat','PMb','flag','dist']
#                       
#                sumD=(1/((ilat-AQSDF.lat)**2+ (ilon-AQSDF.lon)**2)).sum()*0.9+ (1/((ilat-MODDF.lat)**2+ (ilon-MODDF.lon)**2)).sum()*0.1
#                sumN=(AQSDF.PMb/((ilat-AQSDF.lat)**2+ (ilon-AQSDF.lon)**2)).sum()*0.9+ (MODDF.PMb/((ilat-MODDF.lat)**2+ (ilon-MODDF.lon)**2)).sum()*0.1
#    
#
#                
#                IDWres.loc[count].pm=sumN/sumD
#            
#            count=count+1
    
           
                  
    IDWres.to_csv(IDW_final_path , encoding='utf-8', sep='\t', index=False, header=True)        
            
    return IDWres        
            
            