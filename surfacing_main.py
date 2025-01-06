# -*- coding: utf-8 -*-
"""
@author: Barik
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

import os 
import config_lib
import modis_mosaic
import MODIS_average
import AQS_QC
import AQS_average
import AQS_selection
import time 
#import MODIS_smooth
#import AQS_smooth
##Bias_correction_v3 
import merge_modis_corrected_and_rawdata
import IDW_Surface        #This is with loops
#import IDW_Surface_v2    #This is without loops (with arrays) to make it more effecient/faster
import wrapper

start=time.time()

if __name__ =="__main__":
    config=config_lib.Config()
    band=config.band
    year=config.year
    slp=config.slp
    intr=config.intr
    slp1=config.slp1
    intr1=config.intr1
    slp2=config.slp2
    intr2=config.intr2
    slp3=config.slp3
    intr3=config.intr3
    latmin=config.latmin
    latmax=config.latmax
    lonmin=config.lonmin
    lonmax=config.lonmax
    xcells=config.xcells
    ycells=config.ycells
    wA=config.wA
    wM=config.wM
    wT=config.wT
    MODIS_data_path=config.MODIS_data_path
    rawdata_output_path=config.rawdata_output_path
    EPA_path=config.EPA_path
    area_name=config.area_name
    pixelsfile_path=config.pixelsfile_path
    cellsizex=config.cellsizex
    cellsizey=config.cellsizey
    ix=config.ix
    iy=config.iy
    QC=config.QC
    
    
    #getting surfacing grids for plotting 
    IDW_cells_path=r'./IDW_surface_cells_coordinates.txt'
    IDWsurfaceCoord=pd.read_csv(IDW_cells_path, sep=',', header=None)
    IDWsurfaceCoord.columns = ['lon','lat']
    shape = np.unique(IDWsurfaceCoord['lat'] ).shape[0], np.unique(IDWsurfaceCoord['lon']).shape[0]
    x_arr = IDWsurfaceCoord['lon'].values.reshape(shape)
    y_arr = IDWsurfaceCoord['lat'].values.reshape(shape)
    
    
    #select station within the region provided 
    print ('\nFetching EPA station locations within the interest area ...')
    AQS_selection.STselection(EPA_path,rawdata_output_path,year, latmax, latmin, lonmin,lonmax, area_name )
    
    
    #process
    count=0
    for day in range(1,3):
        DOY = str('%0.3d' % day)
        print(DOY)
        print ('\n Mosaicing MODIS data ...')
        modis_mosaic.mosaic(day, band, year, slp, intr,slp1, intr1,slp2, intr2,slp3, intr3, latmin, latmax, lonmin, lonmax, xcells, ycells, MODIS_data_path, rawdata_output_path, wM )
        
        
        if (os.path.getsize(rawdata_output_path+ '/' + 'MODIS_rawdata_DOY'+DOY+'.txt') > 0)==True:
        
            MODIS_average.process(rawdata_output_path, latmin, latmax, lonmin, lonmax, xcells, ycells, day, wM, wT)
            
            print ('\n AQS QC ...')
            AQS_QC.AQS_process(EPA_path,rawdata_output_path, area_name, year, latmax, latmin, lonmin,lonmax, xcells, ycells, day, wA )
            #if os.path.exists(rawdata_output_path+'/' + 'AQS_rawdata_noQC_'+year+'_DOY'+DOY+'.txt'):
            AQS_average.process(rawdata_output_path, year, latmax, latmin, lonmin,lonmax, xcells, ycells, day, wT )
    
            #        print ('\n Smoothing data ...')
            #        MODIS_smooth.process(DOY)
            #        AQS_smooth.process(QC,DOY)
                    
            #        print ('\n Bias correction...')
            #        Bias_correction_v3.process(rawdata_output_path, pixelsfile_path, DOY, wM)
            print ('\n Merging MODIS and AQS data...')
            merge_modis_corrected_and_rawdata.process(QC, year, DOY, rawdata_output_path)
            
            print ('\n Running IDW surfacing...')
    
            #IDW_Surface_v2.process(QC,year, cellsizex,cellsizey, ix, iy, latmin, lonmin, DOY)
            IDW_Surface.process(QC, cellsizex,cellsizey, ix, iy, latmin, lonmin, DOY, pixelsfile_path)
            if QC=='yes':
                outfile='./output/Final_Results_IDW_QC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
            else:
                outfile='./output/Final_Results_IDW_noQC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
                
            dailyIDW=pd.read_csv(outfile, header=None, sep='\t')
            
            #print (dailyIDW)
            if count==0:
                AllIDWdata=dailyIDW
                AllIDWdata.columns=['lon','lat','Day'+str(day)]
                
            else:
                dailyIDW.columns=['lon','lat','Day'+str(day)]
                AllIDWdata=pd.concat([AllIDWdata, dailyIDW.iloc[:,-1]], axis=1)
        else:
            print ('\n AQS QC ...')
            AQS_QC.AQS_process(EPA_path,rawdata_output_path, area_name, year, latmax, latmin, lonmin,lonmax, xcells, ycells, day, wA )
            #if os.path.exists(rawdata_output_path+'/' + 'AQS_rawdata_noQC_'+year+'_DOY'+DOY+'.txt'):
            AQS_average.process(rawdata_output_path, year, latmax, latmin, lonmin,lonmax, xcells, ycells, day, wT )

            merge_modis_corrected_and_rawdata.process(QC, year, DOY,rawdata_output_path)
            
            print ('\n Running IDW surfacing...')
    
            #IDW_Surface_v2.process(QC,year, cellsizex,cellsizey, ix, iy, latmin, lonmin, DOY)
            IDW_Surface.process(QC, cellsizex,cellsizey, ix, iy, latmin, lonmin, DOY, pixelsfile_path)
            if QC=='yes':
                outfile='./output/Final_Results_IDW_QC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
            else:
                outfile='./output/Final_Results_IDW_noQC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
                
            dailyIDW=pd.read_csv(outfile, header=None, sep='\t')
            
            #print (dailyIDW)
            if count==0:
                AllIDWdata=dailyIDW
                AllIDWdata.columns=['lon','lat','Day'+str(day)]
                
            else:
                dailyIDW.columns=['lon','lat','Day'+str(day)]
                AllIDWdata=pd.concat([AllIDWdata, dailyIDW.iloc[:,-1]], axis=1)
        
#        print ('\n Running BSpline surfacing...')
#        wrapper.process(QC,DOY,cellsizex,cellsizey)
#        newfile='modeldata4_mod.txt'
#        dailyDF=pd.read_csv(newfile, skiprows=range(0,10), header=None, delim_whitespace=True, skipinitialspace=True)
#        
#        if QC=='yes':
#            outfile='./output/Final_Results_BSline_QC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
#        else:
#            outfile='./output/Final_Results_BSline_noQC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
#        
#        dailyDF.columns=['lon','lat','pm']
#        dailyDF.to_csv(outfile , encoding='utf-8', sep='\t', index=False, header=True)
        
######################  activate for plotting only ###################################        
#        ## for plotting Bspline output
#        shape = np.unique(IDWsurfaceCoord['lat'] ).shape[0], np.unique(IDWsurfaceCoord['lon']).shape[0]
#        x_arr = dailyDF['lon'].values.reshape(shape)
#        y_arr = dailyDF['lat'].values.reshape(shape)
#        z_arr = dailyDF['pm'].values.reshape(shape) 
        
#        if QC=='yes':
#            figname="./plots/BSpline_surface_QC_{}_DOY{}".format(year, DOY)
#        else:
#            figname="./plots/BSpline_surface_noQC_{}_DOY{}".format(year, DOY)
#        
#        fig, ax = plt.subplots(figsize=(10, 8))
#        
#        mp = Basemap(projection='cyl', resolution='l',
#                    llcrnrlon=dailyDF['lon'].min(), llcrnrlat=dailyDF['lat'].min(), urcrnrlon=dailyDF['lon'].max(), urcrnrlat=dailyDF['lat'].max())
#        #mp.shadedrelief(scale=0.5)
#        mp.pcolormesh(x_arr,y_arr, z_arr,
#                                 latlon=True, cmap='Pastel1') #RdBu_r
#        mp.colorbar(location='bottom',pad=0.25)
#        mp.drawparallels(np.arange(int(dailyDF['lat'].min()),int(dailyDF['lat'].max()),5),labels=[1,0,0,0],color='grey')
#        mp.drawmeridians(np.arange(int(dailyDF['lon'].min()),int(dailyDF['lon'].max()+1),5),labels=[0,0,0,1],color='grey')
#        mp.drawcoastlines()
#        mp.drawlsmask(ocean_color='w')
#        mp.drawcountries(linewidth=1.5)
#        mp.drawstates(color='black', linewidth=1.5)
#        
#        #plt.show()
#        fig.savefig(figname)
    

#        if count==0:
#            AllBSdata=dailyDF.iloc[:,0:3]
#            AllBSdata.columns=['lon','lat','Day'+str(day)]
#            
#        else:
#            dailyDF.columns=['lon','lat','Day'+str(day)]
#            AllBSdata=pd.concat([AllBSdata, dailyDF.iloc[:,-1]], axis=1)
#        count=count+1
#    
#    #writing data from all days 
#    AllIDWdata.to_csv('IDW_surfacing_AllDays.txt' , encoding='utf-8', sep=',', index=None, header=True)
#    AllBSdata.to_csv('BSpline_surfacing_AllDays.txt' , encoding='utf-8', sep=',', index=None, header=True)

    print('Total runtime:', (time.time()-start)/60,'minutes.')
