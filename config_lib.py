# -*- coding: utf-8 -*-
"""
@author: 
"""
import os


class Config():
    QC='no' #Aqs quaity control yes or no
    MODIS_data_path='C:/Barik/work/CAARE_2018/MODIS_Data/CA/2020/V6/Aqua_3km/'
    rawdata_output_path='C:/Barik/work/CAARE_2018/surfacing/modular_version_weight_AQS_12pt_20km_12mod_noBC_2020'
    if not os.path.exists(rawdata_output_path): 
        os.makedirs(rawdata_output_path)
    
    EPA_path = 'C:/Barik/work/CAARE_2018/EPA_AQS_data//'
    
    pixelsfile_path=r'Bspline_Pixels_Corners.txt' # pixel corner lat lon
    
    area_name=str('SelectedStations') #name of the foder where name of all the AQS station within the region will be
    
    band=str(0.55) ### input('Which band would you like to use (0.47/0.55/0.66)?: ')
    
    ##Bounding box of the the region 
    latmin=float(24.2961)
    latmax=float(49.661)
    lonmin=float(-124.985)
    lonmax=float(-66.965)
    
    year=str(2020)
    print ('Year running for:'+year)
    xcells=int(12) #number of cells in x direction
    ycells=int(12) #number of cells in y direction 

    cellsizey=float(0.036789298) 
    cellsizex=float(0.037157191)

    ix=int(1935)
    iy=int(840)
    
    #slp=float(8.209492276)
    #intr=float(10.21917941)
    
    
#    slp=float(7.941) #all
#    intr=float(9.509)
#    slp1=float(8.390) #lat gt 38 lt 42
#    intr1=float(7.60)
#    slp2=float(8.209492276) #lat gt 35 lt 38
#    intr2=float(10.21917941)
#    slp3=float(7.22) #lat gt 32 lt 35
#    intr3=float(10.709)
    
    slp=float(7.941) #all
    intr=float(9.509)
    slp1=float(7.941) #lat gt 38 lt 42 #Tested on Jan 30, 2019 for all the same equation 
    intr1=float(9.509)
    slp2=float(7.941) #lat gt 35 lt 38 #Tested on Jan 30, 2019 for all the same equation
    intr2=float(9.509)
    slp3=float(7.941) #lat gt 32 lt 35 #Tested on Jan 30, 2019 for all the same equation
    intr3=float(9.509)
    
    wA='  0.10D+1' #AQS data weight 
    wM='  0.010D+1' #MODIS data weight
    wT='  0.025D+1' #average data weight