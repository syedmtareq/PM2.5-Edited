#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:21:41 2017

@author: barik
"""

import os 
import subprocess
import time



def process(QC,DOY, cellsizex, cellsizey):
    
    print('begining of Bspline subroutine')
    print('-----------------------------------')
    
    knotsx=[3,7,15,31]
    knotsy=[3,7,15,31]
    



    #for i in range(1,5):
    #    out=r'./{}run.out'.format(i)
    #    with open(out, 'w') as f:
    #        f.close()
    
    fp = open("boilerplate_modeldata_header.txt") #open the header file 
    for i, line in enumerate(fp):
        if i == 7:
            info=line
            #print(info)
            
            
    for i in range(1,5): # run only first two iterations for smoothing  
        #print(i)
    
        
        xcells=(knotsx[i-1]+1)*2
        ycells=(knotsy[i-1]+1)*2
        if i==int(4):
            xcells=int(300)
            ycells=int(300)
            #print (xcells,ycells)
        #else:
            #print (xcells,ycells)
       
        if QC=='yes':
            file=r'boilerplate_Control_{}th_QC_PM_modis.txt'.format(i)
        else:
            file=r'boilerplate_Control_{}th_noQC_PM_modis.txt'.format(i)
        out=r'{}run_mod.txt'.format(i) #C:\\Barik\\usra\\surfacing_test\\test1\\
        log=r'{}log_mod.txt'.format(i)
    
    
    
    
        with open(log, 'w') as output_f:
          p= subprocess.Popen('MySurf_Mar162005.exe {} {}'.format(file, out),
                             stdout=output_f,
                             stderr=output_f)
    
        ##### Writing input file for next iteration #######################
        newfile=r'modeldata{}_mod.txt'.format(i) #input file for next iter 
        
        if os.path.exists(newfile):
            os.remove(newfile)
        fp = open("boilerplate_modeldata_header.txt") #open the header file 
        f = open(newfile, "a")
        for line in fp:
            #print (line)
            f.write(line)
    
        with open(newfile, 'a') as f:        
            f.write('  '+str(xcells*ycells)+'                        Number of data points                       i7')
            f.write('\n')
        
        #if i==4:    
        time.sleep(5)    
        fout=open(out) #os.getcwd()+'\\'+out
        f = open(newfile, "a")
        for line in fout:
            pieces=line.split()
            num1=pieces[0].replace("D", "E") # converting fortran scientific format to python scitific format 
            num2=pieces[1].replace("D", "E") # converting fortran scientific format to python scitific format 
            num3=pieces[2].replace("D", "E") # converting fortran scientific format to python scitific format 
            f.write('\t'+format(float(num1),'.6f')+ '\t'+format(float(num2),'.6f')+ '\t'+format(float(num3),'.6f')+'\n') # only the pm2.5 value and converted to float 
         


            #print (line)
           # f.write(line)
    #    with open(out,'r') as f1:
    #        with open(newfile, 'a') as f2:
    #            for line in f1:
    #               f2.write(line) 
    
       
        fout.close()
        f.close()