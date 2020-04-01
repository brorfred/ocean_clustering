# Add a region mask (custmize as needed to Longhurst, basins etc..)

# No mask
regmskDar=np.ones(np.shape(omskDar) );
regmskGeo=np.ones(np.shape(omskGeo) );
mskname='none'

# Example mask - North Atlantic
natlmask=0
if natlmask == 1:
  regmskDar=   np.where(darDS.Latitude[0,:,:].values >22 ,1,np.nan) \
             * np.where(darDS.Latitude[0,:,:].values <65 ,1,np.nan) \
             * np.where(darDS.Longitude[0,:,:].values>-90,1,np.nan) \
             * np.where(darDS.Longitude[0,:,:].values<  0,1,np.nan)

  regmskGeo=( geoDS.bathymetry[0,:,:]            \
              .where( geoDS.lat>22 )             \
              .where( geoDS.lat<65 )             \
              .where( geoDS.lon>-90 )            \
              .where( geoDS.lon<0 )              \
            ).values
  regmskGeo=np.where(~np.isnan(regmskGeo),1,np.nan)
  mskname='natl'
