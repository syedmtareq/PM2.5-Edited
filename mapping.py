# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 15:01:29 2018

@author: Rabeya
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataDF=pd.read_csv('./results.csv')


#pivotted=dataDF.pivot('lat','lon','IDW')
##pivotted=dataDF.pivot('lat','lon','IDW')
#
#
#ax=sns.heatmap(pivotted,cmap='Reds')
#ax.invert_yaxis()
#figname="IDW004.jpeg"
##figname="IDW.jpeg"
#plt.tight_layout()
#ax.figure.savefig(figname)
#plt.clf()
#
##plt.scatter(dataDF['lon'], dataDF['lat'],dataDF['Bspline'])
##plt.colorbar()
#plt.show()
#
#dataDF=pd.read_csv('./rawdatalog_IDW_final.txt', sep='\t', header=None) 
#
#pivotted2=dataDF.pivot(2,1,3)
##pivotted=dataDF.pivot('lat','lon','IDW')
#
#
#ax=sns.heatmap(pivotted2,cmap='Reds')
#ax.invert_yaxis()
#figname="observed.jpeg"
##figname="IDW.jpeg"
#plt.tight_layout()
#ax.figure.savefig(figname)
#plt.clf()

#df=pd.read_csv('C:\Barik\Surfacing_Barik\Surfacing_FORTRAN_Codes_Copy_June2018\Miscellaneous\Final_Results_Bspline_Surface_all_days_unlimitted_PM2016_no_text.out')
#
#dataDF['Bspline']=df[0:89999]
#pivotted3=dataDF.pivot('lat','lon','Bspline')
#ax=sns.heatmap(pivotted3,cmap='Reds')
#ax.invert_yaxis()
#figname="Bspline_old.jpeg"
##figname="IDW.jpeg"
#plt.tight_layout()
#ax.figure.savefig(figname)
#plt.clf()

## for old IDW
dataDF=pd.read_csv('./results.csv')
dfIDW=pd.read_csv('C:\Barik\Surfacing_Barik\Surfacing_FORTRAN_Codes_Copy_June2018\Miscellaneous\Final_Results_IDW_Surface_all_days_unlimitted_PM2016_no_text.out')

df=pd.DataFrame(dfIDW[270000:360000],columns=None)

newDF=pd.concat([dataDF,df],axis=1)
pivotted3=newDF.pivot('lat','lon','IDW')
ax=sns.heatmap(pivotted3,cmap='Reds')
ax.invert_yaxis()
figname="IDW_old.jpeg"
#figname="IDW.jpeg"
plt.tight_layout()
ax.figure.savefig(figname)
plt.clf()



