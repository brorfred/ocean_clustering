#This script will attempt to apply the Jackson classifier to the DARWIN reflectance data

using Plots, Distributions, NetCDF, NCDatasets, Interpolations


##This is Gael's Code, taken from 05-OceanColourClassifiers.ipynb##

function fcm(M,Sinv,Rrs)
    f=Array{Any,1}(undef,length(M))
    for ii=1:length(M)
        X=vec(Rrs)-M[ii]
        Z=transpose(X)*Sinv[ii]*X
        f[ii]=ccdf(Chisq(6),Z)
    end
    f
end

function getJackson(file)
    #Jackson et al 2017:
    tmpM = ncread("J17.nc", "cluster_means")
    tmpSinv = ncread("J17.nc", "inverse_covariance")
    wv_cci=[412, 443, 490, 510, 555, 670]
    M=Array{Any,1}(undef,14)
    Sinv=Array{Any,1}(undef,14)
    for ii=1:length(M)
        M[ii]=vec(tmpM[ii,:])
        Sinv[ii]=tmpSinv[1:6,1:6,ii]
    end

    J17=Dict("M" => M, "Sinv" => Sinv, "S" => inv.(Sinv))
    #plot(wv_cci,M,w=3); xlabel!("nm"); ylabel!("Rrs")


    ds = Dataset(file)

    Rrs_412=ds["Rrs412"]
    Rrs_443=ds["Rrs443"]
    Rrs_490=ds["Rrs490"]
    Rrs_510=ds["Rrs510"]
    Rrs_555=ds["Rrs555"]
    Rrs_670=ds["Rrs670"]

    Rrs_412=Rrs_412[1:4:720,1:4:360,1:4:12]
    Rrs_443=Rrs_443[1:4:720,1:4:360,1:4:12]
    Rrs_490=Rrs_490[1:4:720,1:4:360,1:4:12]
    Rrs_510=Rrs_510[1:4:720,1:4:360,1:4:12]
    Rrs_555=Rrs_555[1:4:720,1:4:360,1:4:12]
    Rrs_670=Rrs_670[1:4:720,1:4:360,1:4:12]

    tmp=fill(false,size(Rrs_412))
    for ii in eachindex(Rrs_412)
        !ismissing(Rrs_412[ii]) ? tmp[ii]=!ismissing(Rrs_443[ii].*Rrs_490[ii].*Rrs_510[ii].*Rrs_555[ii].*Rrs_670[ii]) : nothing
    end
    ii=findall(tmp)
    sz=size(Rrs_412)
    #export ii, sz, Rrs_412, Rrs_443, Rrs_490, Rrs_510, Rrs_555, Rrs_670
    mbrshp=Array{Float64,4}(undef,(sz[1],sz[2],sz[3],14));
    for jj=1:length(ii); 
        kk=ii[jj]
        Rrs_tmp=[Rrs_412[kk] Rrs_443[kk] Rrs_490[kk] Rrs_510[kk] Rrs_555[kk] Rrs_670[kk]]
        mbrshp[kk[1],kk[2],kk[3],:]=fcm(J17["M"],J17["Sinv"],Rrs_tmp)
        println(kk)
    end
    return mbrshp
end
#path="https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5"
path="https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/"
filegeo="gridded_geospatial_montly_clim_360_720_ver_0_2.nc"
filedarwin="gridded_darwin_montly_clim_360_720_ver_0_2_2.nc"
#run(`wget $path/$file`)
if ~isfile(filegeo)
    download(string(path, filegeo), filegeo)
end
if ~isfile(filedarwin)
    download(string(path, filedarwin), filedarwin)
end

#varnames=["Rirr412", "Rirr443", "Rirr490", "Rirr510", "Rirr555", "Rirr670"]
varnames=["Rrs412", "Rrs443", "Rrs490", "Rrs510", "Rrs555", "Rrs670"]

for n in 1:length(varnames)
    Rirr=ncread(filedarwin, varnames[n])
    tmp=Rirr/3
    Rrs0=(0.52*tmp)./(1.0 .-1.7*tmp)
    ncwrite(Rrs0,filedarwin,varnames[n])
    #renameVar(filedarwin,varnames[n],newnames[n])
end

DarwinMembers=getJackson(filedarwin)
GeoMembers=getJackson(filegeo)
export DarwinMembers
export GeoMembers