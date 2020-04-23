# Ocean Clustering
Datasets, algorithms, and code to develop clustering methods for the global ocean

This project aim to create a internally consistent dataset observed and modelled ocean properties to be used when developing and testing geophysical clustering approaches. We will provide both data and code to perform the analysis. The dataset consists of monthly climologies resampled to the same 1/2° grid, both gridded in netcdf format and tabulated as hdf5 and csv files. The tabulated data are also provided subsampled by including every 2nd, 4th or 8th datapoint. These files are much smaller to download and work with.  

The effort is done under the auspice of the Simons Collaboration on Computational Biogeochemical Modeling of Marine Ecosystems ([CBIOMES](https://cbiomes.org)), which seeks to develop and apply quantitative models of the structure and function of marine microbial communities at seasonal and basin scales.

### Included Parameters

- Chlorophyll (Chl), PAR, Kd490, Euphotic Depth
- remotely sensed reflectances (Rrs412, Rrs443, Rrs490, Rrs510, Rrs555, Rrs670)
- Sea Surface Temperature (SST), Mixed Layer Depth (MLD)
- Wind Speed (wind), Eddy Kinetik Energy (EKE), Bathymetry

### Remote Sensing Data

These were downloaded from sources listed below and regridded using ... (?)

#### Monthly climatologies (`v0.2.5 alpha`)

Resolution |Gridded | Pandas/hdf5 | Comma separated
---|---|---|---
1/2° | [Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/gridded_geospatial_montly_clim_360_720_ver_0_2.nc) | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_360_720_ver_0_2_5.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_360_720_ver_0_2_5.csv)
 1°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_180_360_ver_0_2_5.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_180_360_ver_0_2_5_5.csv)
2°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_090_180_ver_0_2_5.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_090_180_ver_0_2_5.csv)
4°| | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_045_090_ver_0_2_5.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_045_090_ver_0_2_5.csv)

Netcdf files are identical to the 0.2 version but the csv and tab files includes invalid data. Just remove all NaN's if needed. For example:

```python
pd.read_hdf("https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2_5/tabulated_geospatial_montly_clim_045_090_ver_0_2_5.csv").dropna(inplace=True)
```

#### Data Sources

Variable |Source | DOI
---|---|---
SST | `ESA SST-CCI L4` | `10.5285/62c0f97b1eac4e0197a674870afe1ee6`
Chl | `ESA OC-CCI L4` | `10.5285/9C334FBE6D424A708CF3C4CF0C6A53F5`
PAR | `NASA MODIS L3` | `10.5067/AQUA/MODIS/L3M/PAR/2018`
Kd490 | `NASA MODIS L3` | `10.5067/AQUA/MODIS/L3M/KD/2018`
euphotic_depth | `NASA MODIS L3` | `10.5067/AQUA/MODIS/L3M/ZLEE/2018`
mld | `NOAA PMEL MIMOC` | `10.1002/jgrc.20122`
wind | `NOAA NESDIS`<sup>2</sup> | `10.1029/2006GL027086`
EKE | `OSCAR`<sup>1</sup> | `10.5067/OSCAR-03D01`
bathymetry | `NOAA ETOPO1` | `10.7289/V5C8276M`
Rrs412 | `ESA OC-CCI L4` | `10.5285/9C334FBE6D424A708CF3C4CF0C6A53F5`
Rrs443 | `ESA OC-CCI L4` | `10.5285/9C334FBE6D424A708CF3C4CF0C6A53F5`
Rrs490 | `ESA OC-CCI L4` | `10.5285/9C334FBE6D424A708CF3C4CF0C6A53F5`
Rrs510 | `ESA OC-CCI L4` | `10.5285/9C334FBE6D424A708CF3C4CF0C6A53F5`
Rrs555 | `ESA OC-CCI L4` | `10.5285/9C334FBE6D424A708CF3C4CF0C6A53F5`
Rrs670 | `ESA OC-CCI L4` | `10.5285/9C334FBE6D424A708CF3C4CF0C6A53F5`
---|---|---

<sup>1</sup> Calculated from geostrophic velocities
<sup>2</sup> Blended Sea Winds from [URL](https://www.ncdc.noaa.gov/data-access/marineocean-data/blended-global/blended-sea-winds)

### Model Monthly Climatologies

These were downloaded from the source listed below and regridded using the [gcmfaces](http://gcmfaces.readthedocs.io/en/latest/) toolbox plus recipes from [OceanColorData.jl](https://gaelforget.github.io/OceanColorData.jl/dev/) [(these notebooks)](https://github.com/gaelforget/MarineEcosystemNotebooks) and those included here in `DataSet From DARWIN/`.



Resolution |Gridded | Pandas/hdf5 | Comma separated
---|---|---|---
1/2° | [Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_darwin_montly_clim_360_720_ver_0_2.nc) | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_360_720_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_360_720_ver_0_2.csv)
 1°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_180_360_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_180_360_ver_0_2.csv)
2°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_090_180_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_090_180_ver_0_2.csv)
4°| | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_045_090_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_darwin_montly_clim_045_090_ver_0_2.csv)

**Source:** [DOI](10.5281/zenodo.2653669), [URL](http://engaging-opendap.mit.edu:8080/thredds/dodsC/las/id-fba1de9aef/), [Documentation](https://cbiomes.readthedocs.io/) 

### Standard Classification Estimates

[Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_geospatial_regions_360_720_ver_0_2.nc)

There are still some issues with the hdf and csv files. 
<!--
Resolution |Gridded | Pandas/hdf5 | Comma separated
---|---|---|---
1/2° | [Download cdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/gridded_geospatial_regions_360_720_ver_0_2.nc) | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_360_720_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_360_720_ver_0_2.csv)
 1°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_180_360_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_180_360_ver_0_2.csv)
2°| |[Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_090_180_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_090_180_ver_0_2.csv)
4°| | [Download hdf](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_045_090_ver_0_2.h5) | [Download csv](https://rsg.pml.ac.uk/shared_files/brj/CBIOMES_ecoregions/ver_0_2/tabulated_geospatial_regions_045_090_ver_0_2.csv)
-->
*Included Parameters:* Longhurst, optical\_water\_classes

