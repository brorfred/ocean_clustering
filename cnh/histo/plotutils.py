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

