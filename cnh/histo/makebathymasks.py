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
x1.values=x1.values*omskGeo
xr.plot.imshow(x1)
plt.show()
