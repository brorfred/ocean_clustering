nms=[412,443,490,510,555,670]
nms=[443]

for nm in nms:
 fld='R%d_mask=%s'%(nm,mskname)

 x1=darDS['Rirr%d'%(nm)][mno,:,:]
 x1.values=x1.values*omskDar*regmskDar
 # RRS=(0.52*R/Q)/(1-1.7*R/Q)
 R=x1.values; Q=3.
 RRS=(0.52*R/Q)/(1-1.7*R/Q)
 # RRS=x1.values
 x1.values=RRS

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


