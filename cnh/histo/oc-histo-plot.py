#
# Plot some histograms for fields in https://github.com/brorfred/ocean_clustering
#
# curl https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_geospatial_montly_clim_360_720_ver_0_2.nc > gridded_geospatial_montly_clim_360_720_ver_0_2.nc
# curl https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_darwin_montly_clim_360_720_ver_0_2.nc > gridded_darwin_montly_clim_360_720_ver_0_2.nc
# docker run -P -d --rm -i -t -v `pwd`:/home/jovyan/host jupyter/datascience-notebook 
#  -or-
# curl https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh > Miniconda3-latest-MacOSX-x86_64.sh'
# chmod +x Miniconda3-latest-MacOSX-x86_64.sh 
# ./Miniconda3-latest-MacOSX-x86_64.sh  -b -p `pwd`/miniconda3
# export PATH="`pwd`/miniconda3/bin:$PATH"
# conda create -n ocean-clustering -c conda-forge python=3.7
# 
# . miniconda3/etc/profile.d/conda.sh
# conda activate ocean-clustering
# 
# conda install netCDF4
# conda install  numpy
# conda install xarray
# conda install cartopy
#
# python oc-histo-plot.py
# produces .png plots for each compared field 

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs


geoF='gridded_geospatial_montly_clim_360_720_ver_0_2.nc'
darF='gridded_darwin_montly_clim_360_720_ver_0_2.nc'
geoDS = xr.open_dataset(geoF)
darDS = xr.open_dataset(darF)

def mkplot(f1,f2,fld,mno):
    fig=plt.figure(figsize=(10,10))
    
    ax1 = plt.subplot(12,2,(1,7) ) 
    if type(mno) == int:
     ax1.set_title('Dar-%s, month=%d'%(fld,mno))
    if type(mno) == range:
     ax1.set_title('Dar-%s, month=%s'%(fld,'all'))
    fval=np.ravel( f1 )
    fvavg=np.nanmean(fval)
    fvstd=np.nanstd(fval)
    fvmin=np.nanmin(fval)
    fvmax=np.nanmax(fval)
    ax1.hist(fval,nbin)
    
    ax1s = plt.subplot(12,2,11 ) 
    ax1s.set_axis_off()
    ax1s.text(0,0   ,'mean=%f'%(fvavg))
    ax1s.text(0,0.25,' std=%f'%(fvstd))
    ax1s.text(0,0.5 ,' max=%f'%(fvmax))
    ax1s.text(0,0.75,' min=%f'%(fvmin))
    
    ax2 = plt.subplot(12,2,(2,8) )
    if type(mno) == int:
     ax2.set_title('Geo-%s, month=%d'%(fld,mno))
    if type(mno) == range:
     ax2.set_title('Geo-%s, month=%s'%(fld,'all'))
    fval=np.ravel( f2 )
    fvavg=np.nanmean(fval)
    fvstd=np.nanstd(fval)
    fvmin=np.nanmin(fval)
    fvmax=np.nanmax(fval)
    ax2.hist(np.ravel( fval ),nbin )
    
    ax2s = plt.subplot(12,2,12 ) 
    ax2s.set_axis_off()
    ax2s.text(0,0   ,'mean=%f'%(fvavg))
    ax2s.text(0,0.25,' std=%f'%(fvstd))
    ax2s.text(0,0.5 ,' max=%f'%(fvmax))
    ax2s.text(0,0.75,' min=%f'%(fvmin))
    

 
    if type(mno) == int:
     pname='f_%s_m_%d.png'%(fld,mno)
    if type(mno) == range:
     pname='f_%s_m_%s.png'%(fld,'all')
    
    plt.savefig(pname)

mno=range(0,12,1);nbin=50

fld='SST'
f1=darDS.THETA[mno,:,:].values
f2=geoDS.SST[mno,:,:].values
mkplot(f1,f2,fld,mno)

fld='Chl'
f1=darDS.Chl[mno,:,:].values
f2=geoDS.Chl[mno,:,:].values*0.01
mkplot(f1,f2,fld,mno)

fld='PAR'
f1=darDS.PAR[mno,:,:].values
f2=geoDS.PAR[mno,:,:].values*20.
mkplot(f1,f2,fld,mno)

fld='Depth'
f1=darDS['Bottom Depth'][mno,:,:].values
f1=f1[np.where(f1!=0)]
f2=geoDS.bathymetry[mno,:,:].values*-1.
f2=f2[np.where(f2!=-0.)]
mkplot(f1,f2,fld,mno)

fld='MLD'
f1=darDS['MXLDEPTH'][mno,:,:].values
f2=geoDS.mld[mno,:,:].values
mkplot(f1,f2,fld,mno)

fld='R412'
f1=darDS['Rirr412'][mno,:,:].values
f2=geoDS.Rrs412[mno,:,:].values
f2=f2[np.where(f2<=0.12)]
mkplot(f1,f2,fld,mno)

fld='R443'
f1=darDS['Rirr443'][mno,:,:].values
f2=geoDS.Rrs443[mno,:,:].values
f2=f2[np.where(f2<=0.12)]
mkplot(f1,f2,fld,mno)

fld='R490'
f1=darDS['Rirr490'][mno,:,:].values
f2=geoDS.Rrs490[mno,:,:].values
f2=f2[np.where(f2<=0.12)]
mkplot(f1,f2,fld,mno)

fld='R510'
f1=darDS['Rirr510'][mno,:,:].values
f2=geoDS.Rrs510[mno,:,:].values
f2=f2[np.where(f2<=0.12)]
mkplot(f1,f2,fld,mno)

fld='R555'
f1=darDS['Rirr555'][mno,:,:].values
f2=geoDS.Rrs555[mno,:,:].values
f2=f2[np.where(f2<=0.12)]
mkplot(f1,f2,fld,mno)

fld='R670'
f1=darDS['Rirr670'][mno,:,:].values
f2=geoDS.Rrs670[mno,:,:].values
f2=f2[np.where(f2<=0.12)]
mkplot(f1,f2,fld,mno)

fld='Euphotic Depth'
f1=darDS['Euphotic Depth'][mno,:,:].values
f2=geoDS.euphotic_depth[mno,:,:].values
mkplot(f1,f2,fld,mno)

fld='Wind speed'
f1=darDS['Wind Speed'][mno,:,:].values
f2=geoDS.wind[mno,:,:].values
# f2=f2[np.where(f2<50.0)]
mkplot(f1,f2,fld,mno)

fld='KE'
f1=darDS['TKE'][mno,:,:].values
f2=geoDS.EKE[mno,:,:].values
# f2=f2[np.where(f2<50.0)]
mkplot(f1,f2,fld,mno)
