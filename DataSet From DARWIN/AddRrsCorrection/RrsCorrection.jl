using Plots, Distributions, NetCDF, NCDatasets, Interpolations

filename="HalfDegree.nc"
varnames=["Rirr412", "Rirr443", "Rirr490", "Rirr510", "Rirr555", "Rirr670"]
for n in 1:length(varnames)
    Rirr=ncread(filename, varnames[n])
    tmp=Rirr/3
    Rrs0=(0.52*tmp)./(1.0 .-1.7*tmp)
    ncwrite(Rrs0,"HalfDegree.nc",varnames[n])
end
