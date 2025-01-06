#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mbarik
"""
import os
import pandas as pd
import numpy as np

QC='yes'
xcells=300
ycells=300
N=90000 #cell numbers 

##Bounding box of the the region 
latmin=float(31.655)
latmax=float(42.765)
lonmin=float(-124.735)
lonmax=float(-113.735)

outfile='IDW_surfacing_AllDays_v1mod2.txt'

if os.path.exists(outfile):
    os.remove(outfile) 
    
with open(outfile, 'a') as f:
                          f.write('lon')
                          f.write('\t')
                          f.write('lat')
                          f.write('\t')
                          f.write('\n')
for x in range(xcells):
     for y in range(ycells):
         #print( latmin+((latmax-latmin)/(ycells-1))*y ,',', lonmin+((lonmin-lonmin)/(xcells-1))*x)
         with open(outfile, 'a') as f:
                              f.write(str('%0.6f' %(lonmin+((lonmax-lonmin)/(xcells-1))*x)))
                              f.write('\t')
                              f.write(str('%0.6f' %(latmin+((latmax-latmin)/(ycells-1))*y)))
                              f.write('\n')

count=0
for day in range(1, 3):
    DOY = str('%0.3d' % day)
    print(DOY)
    
    check=0
    
    if QC=='yes':
        infile='./output/Final_Results_IDW_QC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
    else:
        infile='./output/Final_Results_IDW_noQC_Surface_DOY{}_v1_mod1.txt'.format(DOY)
    
    

    if os.path.exists(outfile): 
        check=1
        dailyIDW=pd.read_csv(outfile, header=None, sep='\t')
        with open(outfile, 'a') as f:
            f.write('\t')
            f.write('Day'+str(day))
            f.write('\n')
            for i in range(dailyIDW.shape[0]):
                            f.write('\t')
                            f.write(dailyIDW.loc[i][2])
                            f.write('\n')
    else:
        temp = np.full((N, 1), -9999.0); # declaring an matrix with NaN values
        with open(outfile, 'a') as f:
            f.write('\t')
            f.write('Day'+str(day))
            f.write('\n')
            for i in range(len(temp)):
                            f.write('\t')
                            f.write(temp[i])
                            f.write('\n')
                
f.close()
        
#        #dailyIDW=pd.DataFrame(temp, index=np.arange(N), columns=['lon','lat','Day'+str(day)])
#        
#    
#    #print (dailyIDW)
#    if count==0:
#        AllIDWdata=dailyIDW
#        AllIDWdata.columns=['lon','lat','Day'+str(day)]
#        
#    else:
#        dailyIDW.columns=['lon','lat','Day'+str(day)]
#        AllIDWdata=pd.concat([AllIDWdata, dailyIDW.iloc[:,-1]], axis=1)
#        
#    count=count+1



#    if os.path.exists(outfile): 
#        check=1
#        dailyIDW=pd.read_csv(outfile, header=None, sep='\t')
#    else:
#        temp = np.full((N, 3), -9999.0); # declaring an matrix with NaN values 
#        dailyIDW=pd.DataFrame(temp, index=np.arange(N), columns=['lon','lat','Day'+str(day)])
#        
#    
#    #print (dailyIDW)
#    if count==0:
#        AllIDWdata=dailyIDW
#        AllIDWdata.columns=['lon','lat','Day'+str(day)]
#        
#    else:
#        dailyIDW.columns=['lon','lat','Day'+str(day)]
#        AllIDWdata=pd.concat([AllIDWdata, dailyIDW.iloc[:,-1]], axis=1)
#        
#    count=count+1
#    
#    #writing data from all days 
#    AllIDWdata.to_csv('IDW_surfacing_AllDays_v1mod1.txt' , encoding='utf-8', sep=',', index=None, header=True)
##   AllBSdata.to_csv('BSpline_surfacing_AllDays.txt' , encoding='utf-8', sep=',', index=None, header=True)