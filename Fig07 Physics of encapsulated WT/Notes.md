The py and the dat files is to generate the simulation plot in Fig7G
the workflow for Fig7HI is as follows.


get confocal z-stack images

|
|
v

process in python/napari (code1:preprocessing)
this code seprates multiple zorbs into separate files; denoises with light gaussian blur; then allows custom selection of ROI to remove stray cells in the FOV - this is important since otherwise they can inflate the volumes in the channel without being part of the aggregate. 
the resultant file is saved as OME Tif so the metadata is conserved and BiofilmQ can read it. 


|
|
v

use these files to do BiofilmQ segmentation. 
Include preprocessing to remove noise
Include cube-based segmentation for more accurate quantification later
export vtk as well as csv outputs
|
|
v
use the vtk for viz as in fig7DEF
use csv files for analysis such as in Fig7H and I

|
|
v
now, use the csv outputs in code2: clustering analysis
this generated clustering information; 
the contents of this file are present in contcat of concats.csv
Use code 4 plotting ratios and Rg  -- for plotting fig7H


-----
-----


FOR Fig7I
(all the csv files required are placed in subdirectores here)
first use code 3 - remove loose cells ::  one needs to remove span from the loose cells in the RgzA* channel. below is the logic. 
this channel is used to normlize the Radius of encapsulated wt cells
loose cells can incorporate inacuracy. 

The top layer can contain cells that are not truly part of the cluster. These cells vary in number and position. The code3  removes one layer of such cells; any cells below this layer are considered part of the aggregate.
The approach works as follows: the code first identifies a subset of the peripheral cells and determines their span along the z-axis (referred to here as the z-range). It then removes all data points within this z-range and saves the resulting dataframe as a new CSV. This filtered dataset is suitable for downstream normalization.
The code also includes visualization functions, supporting both batch and individual outputs.

this rgzA* channel radius is used to normalize the wt clusters' radii. 


|
|
v

these files are then used code 4 plotting ratios and Rg
