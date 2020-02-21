
using Plots, Distributions, NetCDF, NCDatasets, Interpolations, Roots

name="C:\\Users\\folle\\Documents\\CBIOMES\\interp"
    
    bdepth=ncread("BottomDepth.nc","Bottom Depth")
    PAR=ncread(name*"\\IrradianceReflectance\\PAR.0001.nc","PAR");
    dept=ncread(name*"\\IrradianceReflectance\\PAR.0001.nc","dep");
    s1, s2, s3, s4 = size(PAR,1), size(PAR,2), size(PAR,3), size(PAR,4)        
    PARs=PAR[:,:,1,:]
    Eudepth=zeros(size(bdepth))
    tmp=PAR
    #tmp=Array{Float64,4}(undef,s1,s2,s3,s4)
    for n in collect(1:s3)
        tmp[:,:,n,:]=tmp[:,:,n,:]./PARs
    end
    export bdepth, tmp, dept, Eudepth
    for n in 1:720
        for m in 1:360
            for o in 1:12
                #export n, m, o
                #The negative in the tmp variable is to make the PAR strictly increasing
                if ~(bdepth[n,m,o]==0)
                    bd=bdepth[n,m,o]
                    if minimum(tmp[n,m,dept.<bd,o])<.01
                    #  println("made it")
                     md=(minimum(dept[tmp[n,m,:,o].<=.01]))
                    # itp=LinearInterpolation(-tmp[n,m,dept.<=md,o],dept[dept.<=md])
                    #  plot(-tmp[n,m,t.==0,o],dept[t.==0])
                    #  println("yes")             
                     Eudepth[n,m,o]=md
                        # d=diff(tmp[n,m,:,o])
                        # D=zeros(length(d)+1)
                        # D[1:length(d)]=d
                        # t=cumsum(D.>=0)
                        # # println(t)
                        # #  println(size(dept.<bd))
                        # # println([n m o])
                        # println(dept[t.=0])
                        # itp=LinearInterpolation(-tmp[n,m,t.==0,o],dept[t.==0])
                        # plot(-tmp[n,m,t.==0,o],dept[t.==0])
                        # println("yes")             
                        # Eudepth[n,m,o]=itp.(-.01)
                        # #itp=LinearInterpolation(dept[dept.<bd],tmp[n,m,dept.<bd,o])
                        # #Eudepth[n,m,o]=find_zero(itp,10)                    
                    end
                end
            end
        end
    end
    if isfile("EuphoticDepth.nc")
         rm("EuphoticDepth.nc")
    end
    nccreate("EuphoticDepth.nc", "Euphotic Depth","Lon",collect(.5:.5:360),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
    ncwrite(Eudepth,"EuphoticDepth.nc", "Euphotic Depth")
    export Eudepth