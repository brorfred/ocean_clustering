#This module/script is intended to mine the CBIOMES-Global Atlas for a specific set of variables which we will
#regrid and put into a single NetCDF files function MakeMasterHalf() will make the master NetCDF file for the half degree grid. Function
#MakeDarwinGrid(deg,names) takes the grid degrees and the variable names and generates the netCDF files for the other resolutions.
Module

using Plots, Distributions, NetCDF, NCDatasets, Interpolations

function MakeMasterHalf()
    #This is the starting folder for the Climatology
    #name="C:\\Users\\folle\\Dropbox (MIT)\\201805-CBIOMES-climatology\\interp"
    name="C:\\Users\\folle\\Documents\\CBIOMES\\interp"
    #name="/nfs/cnhlab001/cnh/cbiomes/201805-CBIOMES-climatology/interp/"
    
    #This is the filename for the .5 degree monthly climatology
    filename="HalfDegree.nc"
    #These are the variable names which we would like on the grid
    #Lat, lon, time, T, S, PAR, Wave Bands, Chl, mixed layer depth, *bottom depth*,
    #Wind Speed, *Ekman pumping*, *Kd*, *Euphotic Depth*, and Eddy Kinetic Energy
    varnamest=["THETA", "SALT", "Rirr001", "Rirr002", "Rirr003", "Rirr004", "Rirr005",
    "Rirr006", "Rirr007", "Rirr008", "Rirr009", "Rirr010", "Rirr011", "Rirr012", "Rirr013", "Chl",
    "MXLDEPTH", "EXFwspee", "GGL90TKE","PAR"]

    # Check if .nc file exists
    if isfile(filename)
        # Open a file as read-only
        ds = Dataset(filename,"r")
        varnames=[]
        println("1")
        println(length(varnamest))
        for n in 1:length(varnamest)
            # check if a file has a variable with a given name
            if ~haskey(ds,varnamest[n])
            push!(varnames,varnamest[n])
            end
        end
    end
    if ~isfile(filename)
    varnames=varnamest
    end
    println(varnames)
    #This is the single giant array
    Tg=Array{Float64,4}(undef,720,360,12,length(varnames))

    #This part of the code generates an array of paths to the individual files
    A=[]
    for (root, dirs, files) in walkdir(name)
            for file in files
                if occursin(r".nc$", file) 
                append!(A,[joinpath.(root, file)]) 
                end
            end
        end

    #This Part searches for the individual files for each data type and extracts the 
    #surface layer only. If there are multiple files the code sums them!
    for m in 1:length(varnames)
        fieldsort=varnames[m]
        b=[]
        field=[]
        for n in 1:length(A)
                        if occursin(fieldsort,A[n]) append!(b,n)
                        end
        end
        B=A[b]
        #B=B[1:5]
        for n in 1:length(B)
            f=[first(split(basename(B[n]),"."))]
            println(varnames[m])
            append!(field,f)
        end
        #println(field)
        tmp=ncread(B[1],field[1])
        println(B[1])
        println(field[1])
        println(size(tmp))
        if length(size(tmp))==4
            tmp=tmp[:,:,1,:]
        end
        T=tmp
        if length(B)>1
            s1, s2, s3 = size(tmp,1), size(tmp,2), size(tmp,3)
            T=Array{Float64,4}(undef,s1,s2,s3,length(B))
            for n in 1:length(B)
                tmp=ncread(B[n],field[n])
                println(size(tmp))
                if length(size(tmp))==4
                    T[:,:,:,n]=tmp[:,:,1,:]
                end
                if length(size(tmp))==3
                    T[:,:,:,n]=tmp
                end
            end
            T=sum(T,dims=4)
        end
        T=T[:,:,:]
        Tg[:,:,:,m]=T
        nccreate(filename, fieldsort,"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
        ncwrite(T,filename, fieldsort)
    end

    #This Part of the code interpolates the Darwin remote reflectance bands to get the occi bands
    wv_cci=[412, 443, 490, 510, 555, 670] #cci wavebands
    wv_drwn3=[400,425,450,475,500,525,550,575,600,625,650,675,700];#DARWIN wavebands
    wbcci=Array{Float64,4}(undef,720,360,12,6)
    wbdrwn=Array{Float64,4}(undef,720,360,12,length(wv_drwn3))
    dwnbands=["Rirr001", "Rirr002", "Rirr003", "Rirr004", "Rirr005",
    "Rirr006", "Rirr007", "Rirr008", "Rirr009", "Rirr010", "Rirr011", "Rirr012", "Rirr013"]
    #export dwnbands, wbdrwn,filename,dwnbands
    for n in 1:length(wbdrwn[1,1,1,:])
        wbdrwn[:,:,:,n]=ncread(filename,dwnbands[n])
    end
    #using Interpolations to interpolate bands (currently linear)
    for n in 1:720
        for m in 1:360
            for o in 1:12
                itp=LinearInterpolation(wv_drwn3,wbdrwn[n,m,o,:])
                wbcci[n,m,o,:]=itp.(wv_cci)
            end
        end
    end
    #export wbcci
    #[412, 443, 490, 510, 555, 670]
    OCCIbands=["Rirr412", "Rirr443", "Rirr490", "Rirr510", "Rirr555",
    "Rirr670"]
    #export OCCIbands
    if isfile("InterpedWavebands3.nc")
        rm("InterpedWavebands3.nc")
    end
    if ~isfile("InterpedWavebands3.nc")
        for n in 1:6
        nccreate("InterpedWavebands3.nc", OCCIbands[n],"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
        ncwrite(wbcci[:,:,:,n],"InterpedWavebands3.nc", OCCIbands[n])
        end
    end
    ## This part gets the bottom depth by finding the first grid cell where the Temperature field does not exist
    dept=ncread(name*"\\PhysicalOceanography\\THETA.0001.nc","dep");
    tem=ncread(name*"\\PhysicalOceanography\\THETA.0001.nc","THETA");
    depth=zeros(length(dept)+1);
    depth[2:end]=dept;
    ind=(length(depth) .- sum(isnan.(tem), dims=3));
    bdepth=permutedims(depth[ind],[1, 2,4,3]);
    bdepth=bdepth[:,:,:];
    if isfile("BottomDepth.nc")
        rm("BottomDepth.nc")
    end
    nccreate("BottomDepth.nc", "Bottom Depth","Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
    ncwrite(bdepth,"BottomDepth.nc", "Bottom Depth")
    
    ## This part finds the 'Euphotic Depth' which we define as the location where PAR is at 1% of its original value
    # export bdepth
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
    # export bdepth, tmp, dept, Eudepth
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
    nccreate("EuphoticDepth.nc", "Euphotic Depth","Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
    ncwrite(Eudepth,"EuphoticDepth.nc", "Euphotic Depth")
    #lon lat depth t


    #OK, now I will unpack the variables, and create a master netcdf file at half degree resolution
    if isfile("MasterHalf.nc")
        rm("MasterHalf.nc")
    end
    #These are the variable names which we would like on the grid
    #Lat, lon, time, T, S, *PAR*, Wave Bands, Chl, mixed layer depth, bottom depth,
    #Wind Speed, *Ekman pumping*, *Kd*, *Euphotic Depth*, and Eddy Kinetic Energy

    #We have everything except PAR, Ekman pumping, Kd, and Euphotic Depth.
    vars=["THETA", "SALT", "Chl", "Rirr412", "Rirr443", "Rirr490", "Rirr510", "Rirr555",
    "Rirr670","MXLDEPTH","Bottom Depth", "EXFwspee", "GGL90TKE","PAR","Euphotic Depth"]
    realnames=["SST", "SALT", "Chl", "Rrs412", "Rrs443", "Rrs490", "Rrs510", "Rrs555",
    "Rrs670","MLD","Bathymetry", "wind", "EKE","PAR","Euphotic Depth"]
    #export vars
    Tg=Array{Float64,4}(undef,720,360,12,length(vars))
    for n in [1 2 3]
        Tg[:,:,:,n]=ncread("HalfDegree.nc",vars[n])
        nccreate("MasterHalf.nc", realnames[n],"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))   
        ncwrite(Tg[:,:,:,n],"MasterHalf.nc", realnames[n])
    end
    for n in [4 5 6 7 8 9]
        Tg[:,:,:,n]=ncread("InterpedWavebands3.nc",vars[n])
        #println("dm")
        nccreate("MasterHalf.nc", realnames[n],"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
        #println("dm dm")
        ncwrite(Tg[:,:,:,n],"MasterHalf.nc", realnames[n])
        #println("dm dm dm")
    end
    for n in [10]
        Tg[:,:,:,n]=ncread("HalfDegree.nc",vars[n])
        nccreate("MasterHalf.nc", realnames[n],"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
        ncwrite(Tg[:,:,:,n],"MasterHalf.nc", realnames[n])
    end
    for n in [11]
        Tg[:,:,:,n]=ncread("BottomDepth.nc",vars[n])
        nccreate("MasterHalf.nc", realnames[n],"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
        ncwrite(Tg[:,:,:,n],"MasterHalf.nc", realnames[n])
    end
    for n in [12 13 14]
        Tg[:,:,:,n]=ncread("HalfDegree.nc",vars[n])
        nccreate("MasterHalf.nc", realnames[n],"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
        ncwrite(Tg[:,:,:,n],"MasterHalf.nc", realnames[n])
    end
    for n in [15]
        Tg[:,:,:,n]=ncread("EuphoticDepth.nc",vars[n])
        nccreate("MasterHalf.nc", realnames[n],"Lon",collect(-179.75:.5:179.75),"Lat",collect(-89.75:.5:89.75),"Month",collect(1:12))
        ncwrite(Tg[:,:,:,n],"MasterHalf.nc", realnames[n])
    end
end


function MakeDarwinGrid(deg,names)
    if isfile("DarwinGrid"*string(deg)*".nc")
        rm("DarwinGrid"*string(deg)*".nc")
    end
    k=keys(Dataset("MasterHalf.nc"))
    for n in 1:length(names)
        if sum(k.==names[n])>=1
            vartmp=ncread("MasterHalf.nc",names[n])
            nccreate("DarwinGrid"*string(deg)*".nc", names[n],"Londim",collect(-179.75:deg:179.75),"Latdim",collect(-89.75:deg:89.75),"Monthdim",collect(1:12))
            #println(size(vartmp[1:Int(deg/.5):end,1:Int(deg/.5):end,:]))
            #println(size(vartmp))
            tmp=vartmp[1:Int(deg/.5):end,1:Int(deg/.5):end,:];
            #println(size(tmp))
            #println(n)
            #println(names[n])
            #export n, tmp, names
            #println(sztmp)
            println(size(tmp))
            ncwrite(tmp,"DarwinGrid"*string(deg)*".nc", names[n])
        end
        if sum(k.==names[n])==0
            tmp=zeros(length(collect(-179.75:deg:179.75)), length(collect(-89.75:deg:89.75)),12)
            if names[n]=="Latitude"
                Lat=collect(-89.75:deg:89.75);
                for m in 1:length(Lat)
                    #fill!(HalfDegree[:,n,:,1],Lat[n])
                    tmp2=fill(Lat[m],size(tmp[:,m,:]))
                    tmp[:,m,:]=tmp2
                end
                nccreate("DarwinGrid"*string(deg)*".nc", names[n],"Londim",collect(-179.75:deg:179.75),"Latdim",collect(-89.75:deg:89.75),"Monthdim",collect(1:12))
                ncwrite(tmp,"DarwinGrid"*string(deg)*".nc", names[n])
                sztmp=size(tmp)
            end
            if names[n]=="Longitude"
                Lon=collect(.5:(deg/.5):360);
                for m in 1:length(Lon)
                    #fill!(HalfDegree[:,n,:,1],Lat[n])
                    tmp2=fill(Lon[m],size(tmp[m,:,:]))
                    tmp[m,:,:]=tmp2
                end
                nccreate("DarwinGrid"*string(deg)*".nc", names[n],"Londim",collect(.5:(deg):360),"Latdim",collect(-89.75:(deg):89.75),"Monthdim",collect(1:12))
                ncwrite(tmp,"DarwinGrid"*string(deg)*".nc", names[n])
            end
            if names[n]=="Month"
                Mon=collect(1:1:12);
                for m in 1:length(Mon)
                    #fill!(HalfDegree[:,n,:,1],Lat[n])
                    tmp2=fill(Mon[m],size(tmp[:,:,m]))
                    tmp[:,:,m]=tmp2
                end
                nccreate("DarwinGrid"*string(deg)*".nc", names[n],"Londim",collect(.5:(deg):360),"Latdim",collect(-89.75:(deg):89.75),"Monthdim",collect(1:12))
                ncwrite(tmp,"DarwinGrid"*string(deg)*".nc", names[n])
            end
        end
    end   
end

#realnames=["Latitude","Longitude","Month","THETA", "SALT", "Chl", "Rirr412", "Rirr443", "Rirr490", "Rirr510", "Rirr555",
#"Rirr670","MXLDEPTH","Bottom Depth", "Wind Speed", "TKE"]