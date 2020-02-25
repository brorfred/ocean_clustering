# Ocean Clustering
Datasets, algorithms, and code to develop clustering methods for the global ocean

This project aim to create a internally consistent dataset observed and modelled ocean properties to be used when developing and testing geophysical clustering approaches. We will provide both data and code to perform the analysis. The dataset consists of monthly climologies resampled to the same 1/2° grid, both gridded in netcdf format and tabulated as hdf5 and csv files. The tabulated data are also provided subsampled by including every 2nd, 4th or 8th datapoint. These files are much smaller to download and work with.  

The effort is done under the auspice of the Simons Collaboration on Computational Biogeochemical Modeling of Marine Ecosystems (CBIOMES), which seeks to develop and apply quantitative models of the structure and function of marine microbial communities at seasonal and basin scales.

## Data

### Version 0.2 alpha

#### Monthly climatologies based on observations
Resolution |Gridded | Pandas/hdf5 | Comma separated
---|---|---|---
1/2° | [Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_geospatial_montly_clim_360_720_ver_0_2.nc) | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_360_720_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_360_720_ver_0_2.csv)
 1°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_180_360_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_180_360_ver_0_2.csv)
2°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_090_180_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_090_180_ver_0_2.csv)
4°| | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_045_090_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_montly_clim_045_090_ver_0_2.csv)

*Included Parameters:* Sea Surface Temperature (SST), Chlorophyll (Chl), PAR, Kd490, Euphotic Depth, Mixed Layer Depth (MLD), Wind Speed (wind), Eddy Kinetik Energy (EKE), Bathymetry, Rrs412, Rrs443, Rrs490, Rrs510, Rrs555, Rrs670

#### Monthly climatologies based on model
Resolution |Gridded | Pandas/hdf5 | Comma separated
---|---|---|---
1/2° | [Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_darwin_montly_clim_360_720_ver_0_2.nc) | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_360_720_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_360_720_ver_0_2.csv)
 1°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_180_360_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_180_360_ver_0_2.csv)
2°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_090_180_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_090_180_ver_0_2.csv)
4°| | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_045_090_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_045_090_ver_0_2.csv)

*Included Parameters:* Salinity (SALT); Sea Surface Temperature (SST), Chlorophyll (Chl), PAR, Kd490, Euphotic Depth, Mixed Layer Depth (MLD), Wind Speed (wind), Eddy Kinetik Energy (EKE), Bathymetry, Rrs412, Rrs443, Rrs490, Rrs510, Rrs555, Rrs670

#### Regions and classifications
Resolution |Gridded | Pandas/hdf5 | Comma separated
---|---|---|---
1/2° | [Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_geospatial_regions_360_720_ver_0_2.nc) | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_360_720_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_360_720_ver_0_2.csv)
 1°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_180_360_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_180_360_ver_0_2.csv)
2°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_090_180_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_090_180_ver_0_2.csv)
4°| | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_045_090_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_045_090_ver_0_2.csv)

*Included Parameters:* Longhurst, optical_water_classes

---

### Version 0.1 pre-alpha

#### Monthly climatologies based on observations
Resolution |Gridded | Pandas/hdf5 | Comma separated
---|---|---|---
1/2° | [Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/gridded_geospatial_montly_clim_360_720.nc) | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_360_720.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_360_720.csv)
 1°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_180_360.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_180_360.csv)
2°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_090_180.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_090_180.csv)
4°| | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_045_090.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_1/tabulated_geospatial_montly_clim_045_090.csv)

*Included Parameters:* Sea Surface Temperature (SST), Chlorophyll (Chl), PAR, Wind Speed (wnd), Eddy Kinetik Energy (EKE),Euphotic Depth,Longhurst Region,Mixed Layer Depth (MLD)


#### Monthly climatologies based on model output
