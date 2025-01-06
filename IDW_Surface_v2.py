#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: mbarik
"""
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

def process(QC,year, cellsizex,cellsizey, ix, iy, latmin, lonmin, DOY ):
    print('begining of IDW surfacing subroutine')
    print('-----------------------------------')
    
    nrows=int(300)
    ncols=int(300)
    
        

    #output file name 
    if QC=='yes':
        IDW_final_path=r'./output/Final_Results_IDW_QC_Surface_DOY{}.txt'.format(DOY)
        IDW_final_alldays_path=r'./output/Final_Results_IDW_QC_Surface_all.txt'.format(DOY)
    else:
        IDW_final_path=r'./output/Final_Results_IDW_noQC_Surface_DOY{}.txt'.format(DOY)
        IDW_final_alldays_path=r'./output/Final_Results_IDW_noQC_Surface_all.txt'.format(DOY)
    
    
    
    #reading raw MODIS and AQS data 
    IDW_rawdata_path=r'./MODIS_bias_corrected_and_rawdata.txt'
    rawDF=pd.read_csv(IDW_rawdata_path, sep='\t', header=None)
    rawDF.columns = ['ID', 'lon','lat','PMb']
    dataCoord=rawDF[['lon','lat']].values

    
    #getting surfacing grids 
    IDW_cells_path=r'./IDW_surface_cells_coordinates.txt'
    IDWsurfaceCoord=pd.read_csv(IDW_cells_path, sep=',', header=None)
    IDWsurfaceCoord.columns = ['lon','lat']
    
    #declaring output dataframe 
    IDWres = pd.DataFrame( columns=['lon','lat','PMI'], index=range(ncols*nrows))
    
    #IDW algorithm 
    dist = cdist(IDWsurfaceCoord,
                 dataCoord, 'euclidean')
    invdist=1/dist
    
    sumD=invdist.sum(axis=1)
    
    sN=dist.T/rawDF.PMb[:,None]
    sN=1/sN
    sN=sN.T
    sumN=sN.sum(axis=1)
    
    IDWres.PMI=sumN/sumD
    
    IDWres['lon'] = IDWsurfaceCoord['lon']
    IDWres['lat'] = IDWsurfaceCoord['lat']
            
    

#    shape = np.unique(IDWres['lat'] ).shape[0], np.unique(IDWres['lon']).shape[0]
#    x_arr = IDWres['lon'].values.reshape(shape)
#    y_arr = IDWres['lat'].values.reshape(shape)
#    z_arr = IDWres['PMI'].values.reshape(shape) 
#    
#    if QC=='yes':
#            figname="./plots/IDW_surface_QC_{}_DOY{}".format(year, DOY)
#    else:
#            figname="./plots/IDW_surface_noQC_{}_DOY{}".format(year, DOY)
#    
#
#    fig, ax = plt.subplots(figsize=(10, 8))
#
#    mp = Basemap(projection='cyl', resolution='l',
#                llcrnrlon=IDWres['lon'].min(), llcrnrlat=IDWres['lat'].min(), urcrnrlon=IDWres['lon'].max(), urcrnrlat=IDWres['lat'].max())
#    #mp.shadedrelief(scale=0.5)
#    mp.pcolormesh(x_arr,y_arr, z_arr,
#                             latlon=True, cmap='Pastel1')
#    mp.colorbar(location='bottom',pad=0.25)
#    mp.drawparallels(np.arange(int(IDWres['lat'].min()),int(IDWres['lat'].max()),5),labels=[1,0,0,0],color='grey')
#    mp.drawmeridians(np.arange(int(IDWres['lon'].min()),int(IDWres['lon'].max()+1),5),labels=[0,0,0,1],color='grey')
#    mp.drawcoastlines()
#    mp.drawcountries(linewidth=1.5)
#    mp.drawstates(color='b')
#    
#    #plt.show()
#    fig.savefig(figname)
    
    IDWres.to_csv(IDW_final_path , encoding='utf-8', sep='\t', index=False, header=False)        
            
    return IDWres        
            
            