# Make mask for very high Chl values in Satellite based estimates for open-ocean (depth > dmin )
chlMax=1

phi=geoDS.Chl[:,:,:].values
with np.errstate(invalid='ignore'):
 chlmskGeo=np.where(  phi<chlMax ,1,np.nan)
