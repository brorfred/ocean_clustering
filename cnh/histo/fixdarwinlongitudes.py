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
