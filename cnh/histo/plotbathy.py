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
