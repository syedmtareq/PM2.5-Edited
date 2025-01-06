# -*- coding: utf-8 -*-
"""

@author: Barik
"""
import os 
import calendar
import pandas as pd
import numpy as np
import math

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
            if calendar.isleap(int(pieces[2])) == True: #leap year
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

def STselection(EPA_path,rawdata_output_path, year, lat_up, lat_down, lon_left,lon_right, area_name):
    #print ('\nFetching EPA station locations within the interest area ...')
    


    EPA_dict = {}
    #Storelatlon=[] ### for storing station details from all the years together


    station_path = EPA_path + r'Station_Info/{}//'.format(area_name)
    if not os.path.exists(station_path):
        os.makedirs(station_path)

    EPA_dict[year] = {'lon':[], 'lat':[], 'date':[], 'city':[], 'code':[], 'pm25':[]} 

    with open(EPA_path + year + '.txt') as f:
        f.readline()     
        for line in f:
          fields = line.strip().split("\t")  
          if float(fields[5]) <= lat_up and float(fields[5]) >= lat_down and float(fields[6]) <= lon_right and float(fields[6]) >= lon_left:
            EPA_dict[year]['lon'].append(float(fields[6]))
            EPA_dict[year]['lat'].append(float(fields[5]))
            EPA_dict[year]['date'].append(fields[11])
            EPA_dict[year]['city'].append(fields[26].replace('\'',''))
            EPA_dict[year]['code'].append('{}.{}.{}'.format(fields[0],fields[1],fields[2])) #station code = state.county.side IDs
            EPA_dict[year]["pm25"].append(float(fields[16]))
            
    latlon=set(zip(EPA_dict[year]['lon'], EPA_dict[year]['lat'], EPA_dict[year]['code'], EPA_dict[year]['city'])) #Barik making a list of station coordianes
    #print(latlon)
    # Date convert to DOY
    EPA_dict[year]['date']=julian(EPA_dict[year]['date']) 
    #print(EPA_dict[year]['date'])
    #save all station info for year and area
    with open(station_path + "{}{}.csv".format(area_name, year), "w") as f:
        f.write('lon,lat,code,city\n')
        for row in latlon:
                for r in row:
                    f.write(str(r)+',')
                f.write("\n") 
                
    EPA_raw_pd = pd.DataFrame(EPA_dict[year])
    EPA_raw_pd.to_csv(rawdata_output_path+'//' + 'AQS_rawdata_'+year+'.txt', encoding='utf-8', index=False)

