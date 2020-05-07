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
plot(wv_cci,M,w=3); xlabel!("nm"); ylabel!("Rrs")

#path="https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5"
path="https://https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/"
file="gridded_geospatial_montly_clim_360_720_ver_0_2.nc"
file="gridded_darwin_montly_clim_360_720_ver_0_2_2.nc"
#run(`wget $path/$file`)
download(string(path, file), file)
#Using NCDatasets
#Dataset(file)
#fil="C:\Users\folle\Dropbox (MIT)\CBIOMES_TransitionZone\Chris Follett\StatsGroup\ocean_clustering\DataSet From DARWIN\AddRrsCorrection\HalfDegree.nc"
#fil="C:\\Users\\folle\\Dropbox (MIT)\\CBIOMES_TransitionZone\\Chris Follett\\StatsGroup\\ocean_clustering\\DataSet From DARWIN\\AddRrsCorrection\\HalfDegree.nc"
#dir0="../samples/"
#fil="MasterHalf.nc"
##
varnames=["Rirr412", "Rirr443", "Rirr490", "Rirr510", "Rirr555", "Rirr670"]
for n in 1:length(varnames)
    Rirr=ncread(filename, varnames[n])
    tmp=Rirr/3
    Rrs0=(0.52*tmp)./(1.0 .-1.7*tmp)
    ncwrite(Rrs0,"HalfDegree.nc",varnames[n])
end
##

ds = Dataset(file)

Rrs_412=ds["Rirr412"]
Rrs_443=ds["Rirr443"]
Rrs_490=ds["Rirr490"]
Rrs_510=ds["Rirr510"]
Rrs_555=ds["Rirr555"]
Rrs_670=ds["Rirr670"]

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
export ii, sz, Rrs_412, Rrs_443, Rrs_490, Rrs_510, Rrs_555, Rrs_670
mbrshp=Array{Float64,4}(undef,(sz[1],sz[2],sz[3],14));
for jj=1:length(ii); 
    kk=ii[jj]
    Rrs_tmp=[Rrs_412[kk] Rrs_443[kk] Rrs_490[kk] Rrs_510[kk] Rrs_555[kk] Rrs_670[kk]]
    mbrshp[kk[1],kk[2],kk[3],:]=fcm(J17["M"],J17["Sinv"],Rrs_tmp)
    println(kk)
end
export mbrshp
heatmap(mbrshp[:,:,1,10])