#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mbarik
"""

import os 
import subprocess
import time
def process(DOY):
    knotsx=[3,7,15,31]
    knotsy=[3,7,15,31]
    
    cellsizey=0.03 
    cellsizex=0.03
    
    print('begining of MODIS_smooth_subroutine')
    print('-----------------------------------')
    
    
    fp = open("./boilerplate_modeldata_header.txt") #open the header file 
    for i, line in enumerate(fp):
        if i == 7:
            info=line
            print(info)
            
            
    for i in range(1,5):
        print(i)
     
        
        xcells=(knotsx[i-1]+1)*2
        ycells=(knotsy[i-1]+1)*2
        if i==int(2) or i==int(4):
            xcells=300
            ycells=300
#            print (xcells,',',ycells)
#        else:
#            print (xcells,',',ycells)
       
        
        file=r'boilerplate_Control_{}th_QC_PM_modis_smooth_MODIS.txt'.format(i)
        out=r'{}run_modsm.txt'.format(i)
        log=r'{}log_modsm.txt'.format(i)
    
    
    
    
        with open(log, 'w') as output_f:
          p= subprocess.Popen('MySurf_Mar162005.exe {} {}'.format(file, out),
                             stdout=output_f,
                             stderr=output_f)
    
        ##### Writing input file for next iteration #######################
        newfile=r'modeldata{}_modsm.txt'.format(i) #input file for next iter 
        if os.path.exists(newfile):
            os.remove(newfile)
        fp = open("boilerplate_modeldata_header.txt") #open the header file 
        f = open(newfile, "a")
        for line in fp:
            #print (line)
            f.write(line)
    
        with open(newfile, 'a') as f:        
            f.write('    '+str(xcells*ycells)+'                        Number of data points                       i7')
            f.write('\n')
            
            
        time.sleep(5)
        fout=open(out)
        f = open(newfile, "a")
        for line in fout:
            #print (line)
            f.write(line)    
       
        ##### Writing MODIS smoothed PM2.5 data #######################
        if i==int(2):
            smoothfile=r'MODIS_IDW.txt'
            if os.path.exists(smoothfile):
                os.remove(smoothfile)
                
            fout=open(out)
            f = open(smoothfile, "a")
            for line in fout:
                pieces=line.split()
                num=pieces[2].replace("D", "E") # converting fortran scientific format to python scitific format 
                f.write(' '+format(float(num),'.6f')) # only the pm2.5 value and converted to float 
                f.write('\n')
        fout.close()
        f.close()
        
        if i==int(2):
            smoothfile_DOY=r'./rawdata/MODIS_IDW_{}.txt'.format(DOY)
            if os.path.exists(smoothfile_DOY):
                os.remove(smoothfile_DOY)
                
            foutD=open(out)
            fD = open(smoothfile_DOY, "a")
            for line in foutD:
                pieces=line.split()
                num=pieces[2].replace("D", "E") # converting fortran scientific format to python scitific format 
                fD.write(' '+format(float(num),'.6f')) # only the pm2.5 value and converted to float 
                fD.write('\n')
