# Dataset for Provinces: CBIOMES-global

**Content:**
`Re-Sampled Dataset from CBIOMES-global (alpha version)`

This folder contains the code to build current versions of the .5, 1, 2, and 4 degree gridded, global surface variables from the CBIOMES-global (alpha version). Each variable in the netcdf file is in a matrix A[:,:,:] where the first entry is the longitude, the second is the latitude and the third index is the month.

To generate the netCDF files for the .5, 1, 2, and 4 degree grids (DARWINGrid0.5.nc, DARWINGrid1.0.nc, DARWINGrid2.0.nc, DARWINGrid4.0.nc) first modify the "name" string on line 10 of "MakeGridDarwin2.jl" to be the file system path to the CBIOMES-global atlas. Next, run "Main_MakeGridDarwin2.jl".

- `CBIOMES-global (alpha version)` is a global ocean state estimate that covers the period from 1992 to 2011. It is based on Forget et al 2015 for ocean physics and on Dutkiewicz et al 2015 for marine biogeochemistry and ecosystems with 35 phytoplankton types, 16 zooplankton types, and the allometric relationships of Ward et al 2012. 

This folder contains code written in Julia to generate gridded data for the following variables and a code that will extract/calculate them if given the path to a folder containing the CBIOMES-global Atlas.

- "Lat"             (degrees)
- "Lon"             (degrees)
- "Month"           (month)
- "SST"           (degrees C)
- "SALT"            (psu)
- "Chl"             (mg/l)
- "Rrs412"         (irradiance reflectance for waveband at wavelength)
- "Rrs443"         (irradiance reflectance for waveband at wavelength)
- "Rrs490"         (irradiance reflectance for waveband at wavelength)
- "Rrs510"         (irradiance reflectance for waveband at wavelength)
- "Rrs555"         (irradiance reflectance for waveband at wavelength)
- "Rrs670"         (irradiance reflectance for waveband at wavelength)
- "MLD"        (depth, meters)
- "Bathymetry"    (depth, meters)
- "wind"      (m/s)
- "EKE"             (m^2/s^2) is GGL90 sub-grid turbulent kinetic energy
- "PAR"             () 
- "Euphotic Depth"  Depth (m) where light is 1% of the surface values

**Missing Variables**

The following variables were discussed as part of our master list and are not currently in the netcdf file. We are hoping to rectify that soon. 

- PAR (Photosynthetically Active Radiation)
- Ekman pumping
- Kd
- Euphotic Depth


**References:**

Forget, G., J.-M. Campin, P. Heimbach, C. N. Hill, R. M. Ponte, and C. Wunsch, 2015: ECCO version 4: an integrated framework for non-linear inverse modeling and global ocean state estimation. Geoscientific Model Development, 8, 3071-3104, <http://dx.doi.org/10.5194/gmd-8-3071-2015> or [this URL](http://www.geosci-model-dev.net/8/3071/2015/)

Dutkiewicz, S., A.E. Hickman, O. Jahn, W.W. Gregg, C.B. Mouw, and M.J. Follows, 2015: Capturing optically important constituents and properties in a marine biogeochemical and ecosystem model. Biogeoscience, 12, 4447-4481, <http://dx.doi.org/10.5194/bg-12-4447-2015> or [this URL](https://www.biogeosciences.net/12/4447/2015/)

Ward, B. A., Dutkiewicz, S., Jahn, O., and Follows, M. J., 2012:
A size structured food-web model for the global ocean, Limnol.
Oceanogr., 57, 1877–1891, <https://dx.doi.org/10.4319/lo.2012.57.6.1877> or [this URL](https://aslopubs.onlinelibrary.wiley.com/doi/abs/10.4319/lo.2012.57.6.1877)

**README File Revision History:**

- `2020/01/22 [Chris Follett]` create README file

- `2020/01/22 [Chris Follett]` edited README file
- 
- `2020/02/06 [Chris Follett]` edited README file
