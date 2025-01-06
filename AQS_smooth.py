#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: mbarik
"""

import os 
import subprocess
import time

def process(QC,DOY):

    knotsx=[3,7,15,31]
    knotsy=[3,7,15,31]
    
    cellsizey=0.03 
    cellsizex=0.03
    
    print('begining of AQS_smooth_subroutine')
    print('-----------------------------------')
    #for i in range(1,5):
    #    out=r'./{}run.out'.format(i)
    #    with open(out, 'w') as f:
    #        f.close()
    
    fp = open("boilerplate_modeldata_header.txt") #open the header file 
    for i, line in enumerate(fp):
        if i == 7:
            info=line
            print(info)
            
            
    for i in range(1,5): # run only first two iterations for smoothing  
        print(i)
    
        
        xcells=(knotsx[i-1]+1)*2
        ycells=(knotsy[i-1]+1)*2
        if i==int(2) or i==int(4):
            xcells=300
            ycells=300
            #print (xcells,ycells)
#        else:
#            print (xcells,ycells)
       
        if QC=='yes':
            file=r'boilerplate_Control_{}th_QC_PM_modis_smooth_AQS.txt'.format(i)
        else:
            file=r'boilerplate_Control_{}th_noQC_PM_modis_smooth_AQS.txt'.format(i)
        out=r'{}run_aqssm.txt'.format(i) #C:\\Barik\\usra\\surfacing_test\\test1\\
        log=r'{}log_aqssm.txt'.format(i)
    
    
    
    
        with open(log, 'w') as output_f:
          p= subprocess.Popen('MySurf_Mar162005.exe {} {}'.format(file, out),
                             stdout=output_f,
                             stderr=output_f)
    
        ##### Writing input file for next iteration #######################
        newfile=r'modeldata{}_aqssm.txt'.format(i) #input file for next iter 
        
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
            
        #if i==4:    
        time.sleep(5)   
        fout=open(out) #os.getcwd()+'\\'+out
        f = open(newfile, "a")
        for line in fout:
            #print (line)
            f.write(line)
    #    with open(out,'r') as f1:
    #        with open(newfile, 'a') as f2:
    #            for line in f1:
    #               f2.write(line) 
    
        ##### Writing smoothed PM2.5 data #######################
        if i==int(2):
            smoothfile=r'./AQS_IDW.txt'
            if os.path.exists(smoothfile):
                os.remove(smoothfile)
                
            fout=open(out)
            f = open(smoothfile, "a")
            for line in fout:
                pieces=line.split()
                num=pieces[2].replace("D", "E") # converting fortran scientific format to python scitific format 
                f.write(' '+format(float(num),'.6f')) # only the pm2.5 value and converted to float 
                f.write('\n')
                
        if i==int(2):     
            smoothfile_DOY=r'./rawdata/AQS_IDW_{}.txt'.format(DOY)
            if os.path.exists(smoothfile_DOY):
                os.remove(smoothfile_DOY)
                
            foutD=open(out)
            fD = open(smoothfile_DOY, "a")
            for line in foutD:
                pieces=line.split()
                num=pieces[2].replace("D", "E") # converting fortran scientific format to python scitific format 
                fD.write(' '+format(float(num),'.6f')) # only the pm2.5 value and converted to float 
                fD.write('\n')
    #    fout.close()
    
       
        fout.close()