# -*- coding: utf-8 -*-
"""

@author:
"""

import os 
import pandas as pd


def process(rawdata_output_path, latmin, latmax, lonmin, lonmax, xcells, ycells, day, w, wT ):
    DOY = str('%0.3d' % day)

    #loading merged mosaic data   
    dataDF=pd.read_csv(rawdata_output_path+ '//' + 'MODIS_rawdata_DOY'+DOY+'.txt', sep="\t", header=None) 

    #writing merged MODIS rawdata with header  
    if os.path.exists(rawdata_output_path+ '//' + 'MODIS_rawdata.txt'):
          os.remove(rawdata_output_path+ '//' + 'MODIS_rawdata.txt')
    with open(rawdata_output_path+ '//' + 'MODIS_rawdata.txt', 'w') as f:
                              f.write(w)
                              f.write('\n')
                              f.write('  ')
                              f.write(str(len(dataDF.index)))
                              f.write('\n')
    dataDF.to_csv(rawdata_output_path+ '//' +'MODIS_rawdata.txt',mode='a', header=False, sep='\t', index=False)

    
    ##Average MODIS data over the selected region 
    if not dataDF.empty:
         modis_average_over_region=dataDF[2].mean()
         if os.path.exists(rawdata_output_path+ '//' + 'obsmean16_MODIS.txt'):
                            os.remove(rawdata_output_path+ '//' + 'obsmean16_MODIS.txt') # deleting an already existing file from previous timestep, since appending will be done 
         if not os.path.exists(rawdata_output_path+ '//' + 'obsmean16_MODIS.txt'): #header only for the first loop 
                          with open(rawdata_output_path+ '//' + 'obsmean16_MODIS.txt', 'w') as f:
                              f.write(wT)
                              f.write('\n')
                              f.write('  ')
                              f.write(str(xcells*ycells))
                              f.write('\n')
                
         for x in range(xcells):
           for y in range(ycells):
             #print( latmin+((latmax-latmin)/(ycells-1))*y ,',', lonmin+((lonmin-lonmin)/(xcells-1))*x)
             with open(rawdata_output_path+ '//' + 'obsmean16_MODIS.txt', 'a') as f:
                              f.write('     ')
                              f.write(str('%0.6f' %(lonmin+((lonmax-lonmin)/(xcells-1))*x)))
                              f.write('\t')
                              f.write(str('%0.6f' %(latmin+((latmax-latmin)/(ycells-1))*y)))
                              f.write('\t')
                              f.write(str('%0.6f' %(modis_average_over_region)))
                              f.write('\n')