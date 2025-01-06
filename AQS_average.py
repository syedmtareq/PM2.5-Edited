# -*- coding: utf-8 -*-
"""


@author: 
"""

import os 
import pandas as pd


def process(rawdata_output_path,year, lat_up, lat_down, lon_left,lon_right, xcells, ycells, day, w ): 
        
        DOY = str('%0.3d' % day)
    
        
        #loading no QC AQS data   
        dataDF=pd.read_csv(rawdata_output_path+'//' + 'AQS_rawdata_noQC_'+year+'_DOY'+DOY+'.txt', sep="\t", header=None)
        dataDF.columns=['lon','lat','pm25']
        ##Average AQS data over the selected region no QC
        epa_selected_for_day_average_over_region=dataDF['pm25'].mean()
        if os.path.exists(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt'):
                    os.remove(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt') # deleting an already existing file from previous timestep, since appending will be done 
        if not os.path.exists(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt'): #header only for the first loop 
                  with open(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt', 'w') as f:
                      f.write(w)
                      f.write('\n')
                      f.write('  ')
                      f.write(str(xcells*ycells))
                      f.write('\n')
        
        for x in range(xcells):
            for y in range(ycells):
              #print( lat_down+((lat_up-lat_down)/(ycells-1))*y ,',', lon_left+((lon_right-lon_left)/(xcells-1))*x)
              with open(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt', 'a') as f:
                      f.write('     ')
                      f.write(str('%0.6f' %(lon_left+((lon_right-lon_left)/(xcells-1))*x)))
                      f.write('\t')
                      f.write(str('%0.6f' %(lat_down+((lat_up-lat_down)/(ycells-1))*y )))
                      f.write('\t')
                      f.write(str('%0.6f' %(epa_selected_for_day_average_over_region)))
                      f.write('\n')
                      
        
        #loading QC AQS data   
        dataDF=pd.read_csv(rawdata_output_path+'//' + 'AQS_rawdata_QC_'+year+'_DOY'+DOY+'.txt', sep="\t", header=None)
        dataDF.columns=['lon','lat','pm25']
        
        ##Average AQS data over the selected region after QC
        epa_selected_for_day_average_over_region=dataDF['pm25'].mean()
        if os.path.exists(rawdata_output_path+'//' + 'obsmeanAQS.txt'):
                    os.remove(rawdata_output_path+'//' + 'obsmeanAQS.txt') # deleting an already existing file from previous timestep, since appending will be done 
        if not os.path.exists(rawdata_output_path+'//' + 'obsmeanAQS.txt'): #header only for the first loop 
                  with open(rawdata_output_path+'//' + 'obsmeanAQS.txt', 'w') as f:
                      f.write(w)
                      f.write('\n')
                      f.write('  ')
                      f.write(str(xcells*ycells))
                      f.write('\n')
        
        for x in range(xcells):
            for y in range(ycells):
              #print( lat_down+((lat_up-lat_down)/(ycells-1))*y ,',', lon_left+((lon_right-lon_left)/(xcells-1))*x)
              with open(rawdata_output_path+'//' + 'obsmeanAQS.txt', 'a') as f:
                      f.write('     ')
                      f.write(str('%0.6f' %(lon_left+((lon_right-lon_left)/(xcells-1))*x)))
                      f.write('\t')
                      f.write(str('%0.6f' %(lat_down+((lat_up-lat_down)/(ycells-1))*y )))
                      f.write('\t')
                      f.write(str('%0.6f' %(epa_selected_for_day_average_over_region)))
                      f.write('\n')