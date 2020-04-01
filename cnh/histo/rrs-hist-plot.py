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

exec(open("plotutils.py").read())
exec(open("fixdarwinlongitudes.py").read())
exec(open("makebathymasks.py").read())
exec(open("makeregmask.py").read())
exec(open("makechlmask.py").read())

# exec(open("plotbathy.py").read())
# OK now lets plot some fields for some month
mno=0;

exec(open("plotrrs.py").read())

exit()


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




