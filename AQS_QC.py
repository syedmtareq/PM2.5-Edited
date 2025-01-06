'''
Station locations fetching for regional analysis
Written by Muhammad Barik (2017)
email: muhammad.barik@nasa.gov
'''
import os 
import calendar
import pandas as pd
import numpy as np
import math
#area_name      =    raw_input('Enter selected area name: ')

def julian(days):
    '''
    converts the dates in days (list) from MM/DD/YYYY to an integer 1-366
    '''
    rv = []
    for i in range(len(days)):
        pieces = str(days[i]).split("/")
        d = [int(pieces[0]), int(pieces[1])] #month and day, [12, 31] for Dec 31st
        j = 0
        if d[0] > 1: j+=31
        if d[0] > 2:
            if calendar.isleap(int(pieces[2])) == 'True': #leap year
                j+=29
            else:
                j+=28
        if d[0] > 3: j+=31
        if d[0] > 4: j+=30
        if d[0] > 5: j+=31
        if d[0] > 6: j+=30
        if d[0] > 7: j+=31
        if d[0] > 8: j+=31
        if d[0] > 9: j+=30
        if d[0] > 10: j+=31
        if d[0] > 11: j+=30
        j += d[1]
        rv.append(j)
    return rv

def dist(lat1,long1, lat, lon):
       return math.sqrt((lat1 - lat) ** 2 + (long1 - lon) ** 2)

def nearby_stations(lat1, long1, epa_selected_for_day_mean):

    epa_selected_for_day_mean['dist'] = epa_selected_for_day_mean.apply(
        lambda row: dist(lat1, long1, row['lat'], row['lon']), 
        axis=1)

    #print(epa_selected_for_day.sort_values(['dist'], ascending=True)[0:6])
    sorted_data=epa_selected_for_day_mean.sort_values(['dist'], ascending=True)[0:6].reset_index()
    del sorted_data['index']
    #print (sorted_data)
    boolean=0
    if sorted_data.shape[0]>=6: #do this check only if data from atleast 6 stations are available 
        if ((sorted_data['pm25'].iloc[0]*2 < sorted_data['pm25'].iloc[1]) and (sorted_data['pm25'].iloc[0]*2 < sorted_data['pm25'].iloc[2]) and (sorted_data['pm25'].iloc[0]*2 < sorted_data['pm25'].iloc[3] ) and (sorted_data['pm25'].iloc[0]*2 < sorted_data['pm25'].iloc[4]) and (sorted_data['pm25'].iloc[0]*2 < sorted_data['pm25'].iloc[5] )):
            boolean=1

    return(boolean) # 1 means the condition has not been mate
    


#main
#-------------------------------------------------------------------------------
#                         Read EPA data for bounding box Barik 
#-------------------------------------------------------------------------------

def AQS_process(EPA_path, rawdata_output_path, area_name,year, lat_up, lat_down, lon_left,lon_right, xcells, ycells, day, w ):
    


    #station_path = EPA_path + r'Station_Info/{}//'.format(area_name)
    EPA_raw_pd=pd.read_csv(rawdata_output_path+'//' + 'AQS_rawdata_'+year+'.txt', index_col=False)
    #print (EPA_raw_pd)

    #estimating mean for each stations 
    mean=[]
    epa_grouped=EPA_raw_pd.groupby(['code','date','lat','lon'])['pm25'].mean().reset_index() # PM2.5 data for same for the same station are averaged
    mean=epa_grouped.groupby('code').mean()
    mean=mean.reset_index()
    #del mean['index'] # getting rid of resundant columns 
    del mean['date'] # getting rid of resundant columns 

    #save unique station info for all years 
    
    mean.to_csv(rawdata_output_path+'//' + 'AQS_mean_'+year+'.txt', encoding='utf-8', index=False)

                          
    EPA_df=EPA_raw_pd.rename(columns = {'date':'doy'}) #changing column name from date to doy
    
    #print (EPA_df)
    
    #if os.path.exists(EPA_path + '//'+'rawdata'+'//' + 'AQS_rawdata_QC_'+year+'.txt'):
    #    os.remove(EPA_path + '//'+'rawdata'+'//' + 'AQS_rawdata_QC_'+year+'.txt') # deleting an already existing file since appending will be done 
    
    #quality control 

    DOY = str('%0.3d' % day)
    print (day)
    indices=np.where(np.in1d(EPA_df['doy'],day))

    if np.array(indices).size >0:
        
        epa_selected_for_day =EPA_df.loc[indices[0],:].reset_index()
        #getting averatge of all the radings in a day
        epa_selected_for_day_mean=epa_selected_for_day.groupby(['code','city','doy','lon','lat'])['pm25'].mean().reset_index() # PM2.5 data for same for the same station are averaged
        
        #For witing of no QC AQS data
        
        epa_selected_for_day_mean_noQC=epa_selected_for_day_mean
        
        del epa_selected_for_day_mean_noQC['doy'],epa_selected_for_day_mean_noQC['code'], epa_selected_for_day_mean_noQC['city'] 

        if os.path.exists(rawdata_output_path+'//' + 'AQS_rawdata_noQC_'+year+'_DOY'+DOY+'.txt'):
                    os.remove(rawdata_output_path+'//' + 'AQS_rawdata_noQC_'+year+'_DOY'+DOY+'.txt') # deleting an already existing file from previous timestep, since appending will be done 
        epa_selected_for_day_mean_noQC.to_csv(rawdata_output_path+'//' + 'AQS_rawdata_noQC_'+year+'_DOY'+DOY+'.txt', encoding='utf-8', sep='\t', index=False, mode='a', header=False)

        #writing no QC AQS data again with using a common file name 
        if os.path.exists(rawdata_output_path+'//' + 'AQS_rawdata_noQC.txt'):
                    os.remove(rawdata_output_path+'//' + 'AQS_rawdata_noQC.txt') # deleting an already existing file from previous timestep, since appending will be done 
        if not os.path.exists(rawdata_output_path+'//' + 'AQS_rawdata_noQC.txt'): #header only for the first loop 
                  with open(rawdata_output_path+'//' + 'AQS_rawdata_noQC.txt', 'w') as f:
                      f.write(w)
                      f.write('\n')
                      f.write('  ')
                      f.write(str(len(epa_selected_for_day_mean_noQC)))
                      f.write('\n')
        epa_selected_for_day_mean_noQC.to_csv(rawdata_output_path+'//' + 'AQS_rawdata_noQC.txt', encoding='utf-8', sep='\t', index=False, mode='a', header=False)

        
        
#        ##Average AQS data over the selected region no QC
#        epa_selected_for_day_average_over_region=epa_selected_for_day_mean['pm25'].mean()
#        if os.path.exists(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt'):
#                    os.remove(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt') # deleting an already existing file from previous timestep, since appending will be done 
#        if not os.path.exists(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt'): #header only for the first loop 
#                  with open(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt', 'w') as f:
#                      f.write(w)
#                      f.write('\n')
#                      f.write('  ')
#                      f.write(str(xcells*ycells))
#                      f.write('\n')
#        
#        for x in range(xcells):
#            for y in range(ycells):
#              #print( lat_down+((lat_up-lat_down)/(ycells-1))*y ,',', lon_left+((lon_right-lon_left)/(xcells-1))*x)
#              with open(rawdata_output_path+'//' + 'obsmeanAQSnoQC.txt', 'a') as f:
#                      f.write('     ')
#                      f.write(str('%0.6f' %(lon_left+((lon_right-lon_left)/(xcells-1))*x)))
#                      f.write('\t')
#                      f.write(str('%0.6f' %(lat_down+((lat_up-lat_down)/(ycells-1))*y )))
#                      f.write('\t')
#                      f.write(str('%0.6f' %(epa_selected_for_day_average_over_region)))
#                      f.write('\n')

              


        #apply quality control function, D comes with the decision to keep a data point or not, D=1 means reject, D=0 means keep 
        D=(epa_selected_for_day_mean.apply(
              lambda row: nearby_stations(row['lat'], row['lon'], epa_selected_for_day_mean), 
              axis=1))
        #print (D)
        epa_selected_for_day_mean['boolean']=D
        epa_selected_for_day_mean = epa_selected_for_day_mean[epa_selected_for_day_mean.boolean == 0] # keeping only the data point thta resulted in 0 in quality control 
        #print(epa_selected_for_day_mean)
        # getting rid of redundant columns and writing quality controlled AQS data 
        del  epa_selected_for_day_mean['dist'] ,  epa_selected_for_day_mean['boolean']
        
        
        #writing QC AQS data 
        if os.path.exists(rawdata_output_path+'//' + 'AQS_rawdata_QC_'+year+'_DOY'+DOY+'.txt'):
                    os.remove(rawdata_output_path+'//' + 'AQS_rawdata_QC_'+year+'_DOY'+DOY+'.txt') # deleting an already existing file from previous timestep, since appending will be done 
#        if not os.path.exists(rawdata_output_path+'//' + 'AQS_rawdata_QC_'+year+'_DOY'+DOY+'.txt'): #header only for the first loop 
#                  with open(rawdata_output_path+'//' + 'AQS_rawdata_QC_'+year+'_DOY'+DOY+'.txt', 'w') as f:
#                      f.write(w)
#                      f.write('\n')
#                      f.write(' ')
#                      f.write(str(len(epa_selected_for_day_mean)))
#                      f.write('\n')
        epa_selected_for_day_mean.to_csv(rawdata_output_path+'//' + 'AQS_rawdata_QC_'+year+'_DOY'+DOY+'.txt', encoding='utf-8', sep='\t', index=False, mode='a', header=False)
        
        #writing again with using a common file name 
        if os.path.exists(rawdata_output_path+'//' + 'AQS_rawdata_QC.txt'):
                    os.remove(rawdata_output_path+'//' + 'AQS_rawdata_QC.txt') # deleting an already existing file from previous timestep, since appending will be done 
        if not os.path.exists(rawdata_output_path+'//' + 'AQS_rawdata_QC.txt'): #header only for the first loop 
                  with open(rawdata_output_path+'//' + 'AQS_rawdata_QC.txt', 'w') as f:
                      f.write(w)
                      f.write('\n')
                      f.write('  ')
                      f.write(str(len(epa_selected_for_day_mean)))
                      f.write('\n')
        epa_selected_for_day_mean.to_csv(rawdata_output_path+'//' + 'AQS_rawdata_QC.txt', encoding='utf-8', sep='\t', index=False, mode='a', header=False)
    
    
#        ##Average AQS data over the selected region after QC
#        epa_selected_for_day_average_over_region=epa_selected_for_day_mean['pm25'].mean()
#        if os.path.exists(rawdata_output_path+'//' + 'obsmeanAQS.txt'):
#                    os.remove(rawdata_output_path+'//' + 'obsmeanAQS.txt') # deleting an already existing file from previous timestep, since appending will be done 
#        if not os.path.exists(rawdata_output_path+'//' + 'obsmeanAQS.txt'): #header only for the first loop 
#                  with open(rawdata_output_path+'//' + 'obsmeanAQS.txt', 'w') as f:
#                      f.write(w)
#                      f.write('\n')
#                      f.write('  ')
#                      f.write(str(xcells*ycells))
#                      f.write('\n')
#        
#        for x in range(xcells):
#            for y in range(ycells):
#              #print( lat_down+((lat_up-lat_down)/(ycells-1))*y ,',', lon_left+((lon_right-lon_left)/(xcells-1))*x)
#              with open(rawdata_output_path+'//' + 'obsmeanAQS.txt', 'a') as f:
#                      f.write('     ')
#                      f.write(str('%0.6f' %(lon_left+((lon_right-lon_left)/(xcells-1))*x)))
#                      f.write('\t')
#                      f.write(str('%0.6f' %(lat_down+((lat_up-lat_down)/(ycells-1))*y )))
#                      f.write('\t')
#                      f.write(str('%0.6f' %(epa_selected_for_day_average_over_region)))
#                      f.write('\n')
    
    
    
    
    
    
    
    
    
        
        
        
        
