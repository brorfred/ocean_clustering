#!/usr/bin/env python
# coding: utf-8

# In[18]:


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
# 
# conda install netCDF4
# conda install  numpy
# conda install xarray
# conda install cartopy

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs


# In[19]:


geoF='gridded_geospatial_montly_clim_360_720_ver_0_2.nc'
darF='gridded_darwin_montly_clim_360_720_ver_0_2.nc'
geoDS = xr.open_dataset(geoF)
darDS = xr.open_dataset(darF)

# Make signs on bathymetry consistent
x1=geoDS.bathymetry[:,:,:]
x1.values=x1.values*-1.
geoDS.bathymetry[:,:,:]=x1

# Set number of histogram bins
nbin=50


# In[20]:


# Histogram plot
def mkhplot(f1,f2,fld,mno):
    fig=plt.figure(figsize=(10,10))
    
    ax1 = plt.subplot(12,2,(1,7) ) 
    if type(mno) == int:
     ax1.set_title('Dar-%s, month=%d'%(fld,mno))
    if type(mno) == range:
     ax1.set_title('Dar-%s, month=%s'%(fld,'all'))
    fval=np.ravel( f1 )
    fval=fval[~np.isnan(fval)] 
    fvavg=np.nanmean(fval)
    fvstd=np.nanstd(fval)
    fvmin=np.nanmin(fval)
    fvmax=np.nanmax(fval)
    fvmed=np.nanmedian(fval)
    ax1.hist(fval,nbin)
    
    ax1s = plt.subplot(12,2,11 ) 
    ax1s.set_axis_off()
    ax1s.text(0,0   ,'mean=%f'%(fvavg))
    ax1s.text(0,0.25,' std=%f'%(fvstd))
    ax1s.text(0,0.5 ,' max=%f'%(fvmax))
    ax1s.text(0,0.75,' min=%f'%(fvmin))
    ax1s.text(0,1.0 ,' med=%f'%(fvmed))
    
    ax2 = plt.subplot(12,2,(2,8) )
    if type(mno) == int:
     ax2.set_title('Geo-%s, month=%d'%(fld,mno))
    if type(mno) == range:
     ax2.set_title('Geo-%s, month=%s'%(fld,'all'))
    fval=np.ravel( f2 )
    fval=fval[~np.isnan(fval)] 
    fvavg=np.nanmean(fval)
    fvstd=np.nanstd(fval)
    fvmin=np.nanmin(fval)
    fvmax=np.nanmax(fval)
    fvmed=np.nanmedian(fval)
    ax2.hist(np.ravel( fval ),nbin )
    
    ax2s = plt.subplot(12,2,12 ) 
    ax2s.set_axis_off()
    ax2s.text(0,0   ,'mean=%f'%(fvavg))
    ax2s.text(0,0.25,' std=%f'%(fvstd))
    ax2s.text(0,0.5 ,' max=%f'%(fvmax))
    ax2s.text(0,0.75,' min=%f'%(fvmin))
    ax2s.text(0,1.0 ,' med=%f'%(fvmed))
 
    if type(mno) == int:
     pname='h_%s_m_%d.png'%(fld,mno)
    if type(mno) == range:
     pname='h_%s_m_%s.png'%(fld,'all')
    
    plt.savefig(pname)
    
    plt.show()


# In[21]:


# Lat-lon map plot
def mkxyplot(x1,x2,fld,mno):
    
    fig=plt.figure(figsize=(20,10))
    
    ax=plt.subplot(121)
    xr.plot.imshow(x1)
    ax.set_title('Dar-%s, month=%d'%(fld,mno))
    
    ax=plt.subplot(122)
    xr.plot.imshow(x2)
    ax.set_title('Geo-%s, month=%d'%(fld,mno))
    
    if type(mno) == int:
     pname='xy_%s_m_%d.png'%(fld,mno)
    if type(mno) == range:
     pname='xy_%s_m_%s.png'%(fld,'all')

    plt.savefig(pname)
    plt.show()


# In[22]:


# Check bathymetry
fld='Depth'
x1=darDS['Bottom Depth'][1,:,:]
x2=geoDS.bathymetry[1,:,:]
f1=x1.values
f1=f1[np.where(f1!=0)]
f2=x2.values
f2=f2[np.where(f2!=-0.)]
mkhplot(f1,f2,fld,1)
mkxyplot(x1,x2,fld,1)


# In[23]:


# Fix longitudes from Darwin netCDF 
# for some reasons these are offset and everything east of prime meridian is zero
# Only fix for month zero! Longitudes don't change by month. 
darDS.Londim.values
lons=darDS.Londim.values-180
np.shape(lons)
ny=np.size(darDS.Longitude[0,:,0])
for j in range(ny):
  darDS.Longitude[0,j,:]=lons

( geoDS.bathymetry[0,:,:].where( geoDS.lat>22 ).where( geoDS.lon>-90 ).where( geoDS.lon<0 ) ).values


# In[24]:


# Make some masks for "open ocean" (depth > dmin)
dMin=500.

phi=darDS['Bottom Depth'][1,:,:].values
omskDar=np.where(phi>dMin,1,np.nan)
x1=darDS['Bottom Depth'][1,:,:]
x1.values=x1.values*omskDar
xr.plot.imshow(x1)
plt.show()

phi=geoDS.bathymetry[1,:,:].values
omskGeo=np.where(phi>dMin,1,np.nan)
x1=geoDS.bathymetry[1,:,:]
x1.values=x1.values*omskDar
xr.plot.imshow(x1)
plt.show()

# Add a region mask (custmize as needed to Longhurst, basins etc..)

# No mask
regmskDar=np.ones(np.shape(omskDar) );
regmskGeo=np.ones(np.shape(omskGeo) );
mskname='none'

# Example mask - North Atlantic
natlmask=0
if natlmask == 1:
  regmskDar=   np.where(darDS.Latitude[0,:,:].values >22 ,1,np.nan)            * np.where(darDS.Latitude[0,:,:].values <65 ,1,np.nan)            * np.where(darDS.Longitude[0,:,:].values>-90,1,np.nan)            * np.where(darDS.Longitude[0,:,:].values<  0,1,np.nan)

  regmskGeo=( geoDS.bathymetry[0,:,:]             .where( geoDS.lat>22 )              .where( geoDS.lat<65 )              .where( geoDS.lon>-90 )             .where( geoDS.lon<0 )              ).values
  regmskGeo=np.where(~np.isnan(regmskGeo),1,np.nan)
  mskname='natl'


# In[25]:


# Make mask for very high Chl values in Satellite based estimates for open-ocean (depth > dmin )
chlMax=1

phi=geoDS.Chl[:,:,:].values
with np.errstate(invalid='ignore'):
 chlmskGeo=np.where(  phi<chlMax ,1,np.nan) 


# In[26]:


# OK now lets plot some fields for some month
mno=0;


# In[27]:


fld='SST_mask=%s'%(mskname)
x1=darDS.THETA[mno,:,:]
x1.values=x1.values*omskDar*regmskDar

x2=geoDS.SST[mno,:,:]
x2.values=x2.values*omskGeo*regmskGeo

f1=x1.values
f2=x2.values
mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)


# In[28]:


fld='Chl_mask=%s'%(mskname)
x1=darDS.Chl[mno,:,:]
# Model data has some epsilon negative values, set these to zero 
# (amongst other things they cause xarray imshow to choose a dumb "divergent" color scale)
phi=x1.values
with np.errstate(invalid='ignore'):
 phi=np.where(  phi<=0 ,0,phi) 
x1.values=phi
# Mask to open ocean and region mask
x1.values=x1.values*omskDar*regmskDar

x2=geoDS.Chl[mno,:,:]
# Obs data has a few very high values even in open ocean, so mask these and mask shallow ocean
x2.values=x2.values*chlmskGeo[mno,:,:]
x2.values=x2.values*omskGeo*regmskGeo

f1=x1.values
f2=x2.values

mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)


# In[29]:


fld='PAR_mask=%s'%(mskname)
x1=darDS.PAR[mno,:,:]
# Get rid of points where PAR is exactly 0.
phi=x1.values
with np.errstate(invalid='ignore'):
 phi=np.where(  phi==0 ,np.nan,phi) 
x1.values=phi
x1.values=x1.values*omskDar*regmskDar
f1=x1.values*omskDar

x2=geoDS.PAR[mno,:,:]
x2.values=x2.values*20.*omskGeo*regmskGeo
f2=x2.values

mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)


# In[30]:


fld='MLD_mask=%s'%(mskname)

x1=darDS['MXLDEPTH'][mno,:,:]
x1.values=x1.values*omskDar*regmskDar

x2=geoDS.mld[mno,:,:]
x2.values=x2.values*omskGeo*regmskGeo

f1=x1.values
f2=x2.values
mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)

# Now remake plots, with Dariwn deep convection sites clamped to <400m
dcCap=400
fld='MLD-cap=%d'%(dcCap)
phi=x1.values
with np.errstate(invalid='ignore'):
 phi=np.where( phi>dcCap  ,dcCap,phi) 
x1.values=phi

f1=x1.values
f2=x2.values
mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)


# In[31]:


nms=[412,443,490,510,555,670]

for nm in nms:
 fld='R%d_mask=%s'%(nm,mskname)

 x1=darDS['Rirr%d'%(nm)][mno,:,:]
 x1.values=x1.values*omskDar*regmskDar

 x2=geoDS['Rrs%d'%(nm)][mno,:,:]
 # Mask points with very high irradiance
 # Rhigh=100000000
 # with np.errstate(invalid='ignore'):
 # x2.values=np.where(x2.values<=Rhigh,x2.values,np.nan)
 x2.values=x2.values*omskGeo*regmskGeo

 f1=x1.values
 f2=x2.values
 mkhplot(f1,f2,fld,mno)
 mkxyplot(x1,x2,fld,mno)


# In[32]:


fld='Euphotic Depth_mask=%s'%(mskname)

x1=darDS['Euphotic Depth'][mno,:,:]
x1.values=x1.values*omskDar*regmskDar
x2=geoDS.euphotic_depth[mno,:,:]
x2.values=x2.values*omskGeo*regmskGeo

f1=x1.values
f2=x2.values
mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)


# In[33]:


fld='Wind-speed_mask=%s'%(mskname)

x1=darDS['Wind Speed'][mno,:,:]
x1.values=x1.values*omskDar*regmskDar


x2=geoDS.wind[mno,:,:]
# Mask the few very high wind speed points
whigh=12
with np.errstate(invalid='ignore'):
 x2.values=np.where(x2.values<=whigh,x2.values,np.nan)
x2.values=x2.values*omskGeo*regmskGeo


f1=x1.values
f2=x2.values
# f2=f2[np.where(f2<50.0)]
mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)


# In[34]:


fld='KE_mask=%s'%(mskname)

x1=darDS['TKE'][mno,:,:]
x1.values=x1.values*omskDar*regmskDar

x2=darDS['TKE'][mno,:,:]
x2.values=x2.values*omskGeo*regmskGeo



f1=x1.values
f2=x2.values

# f2=f2[np.where(f2<50.0)]
mkhplot(f1,f2,fld,mno)
mkxyplot(x1,x2,fld,mno)


# In[ ]:




