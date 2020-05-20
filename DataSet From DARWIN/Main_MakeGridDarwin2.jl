#Main_MakeGridDarwin2.jl This script will generate the master half degree netcdf file and then will put it on the other grids using the functions 
#in MakeGridDarwin2.jl

include("MakeGridDarwin2.jl")

#if ~isfile("MasterHalf.nc")
    MakeMasterHalf()
#end
# realnames=["Latitude","Longitude","Month","THETA", "SALT", "Chl", "Rirr412", "Rirr443", "Rirr490", "Rirr510", "Rirr555","Rirr670","MXLDEPTH","Bottom Depth", "Wind Speed", "TKE","PAR","Euphotic Depth"]
# for n in [.5 1 2 4]
# MakeDarwinGrid(n,realnames)
# end