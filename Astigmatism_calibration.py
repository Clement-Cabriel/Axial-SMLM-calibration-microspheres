# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 19:32:00 2016

@author: Clément Cabriel
"""

#-----------------------------------------------------------------------------
# Axial SMLM calibration code
#-----------------------------------------------------------------------------
# June 1st, 2016 (last updated November 11th, 2022)
# AUTHOR:
# Clément Cabriel
# Institut des Sciences Moléculaires d'Orsay (ISMO), Université Paris Sud / CNRS, France
# clement.cabriel@espci.fr , cabriel.clement@gmail.com
#-----------------------------------------------------------------------------
# Code to analyse the data acquired on microspheres coated with fluorophores and generate the calibration curve for the astigmatism
# This code is provided as supporting material for the related article: Clément Cabriel, Nicolas Bourg, Guillaume Dupuis, and Sandrine Lévêque-Fort, 'Aberration-accounting calibration for 3D single-molecule localization microscopy', Optics Letters Vol. 43, Issue 2, pp. 174-177 (2018). DOI: https://doi.org/10.1364/OL.43.000174
# If you use this software, please cite the original article. All further work and publication based on this software should follow the licence terms mentioned in the Github repository
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Python 3.8.0
# Set the parameters below, then run the program
#-----------------------------------------------------------------------------
# INPUT FORMAT
# .txt localization array (column-wise): x, y, width_x, width_y (all values in nm)
#-----------------------------------------------------------------------------
# OUTPUT FORMAT
# 'Results_calibration_astigmatism.txt' (column-wise) z, width_x, width_y, width_x - width_y (all values in nm)
#-----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------
# USER DEFINED PARAMETERS
#-----------------------------------------------------------------------------

path=u"Localization_data_astigmatism.txt"     # Complete path to the .txt localization data file
center=[12540,17190]    # Coordinates of the center of the sphere: =[centerX, centerY] (nm)
radius=7500.0            # Radius of the sphere (nm)

display=2     # Display parameters: =1 to display the point cloud; =2 to display the averaged curve (recommended); =3 to display the number of detected molecules (useful to verify the imaging range); =0 not to display the results
averagingwidth=50.0     # Total width of the sliding window used for the averaging (nm)
depthrange=800.0        # Axial range of the calibration (nm) (should match the depth of imaging)

#-----------------------------------------------------------------------------
# END OF USER DEFINED PARAMETERS
#-----------------------------------------------------------------------------

# Data loading
data=np.genfromtxt(path,delimiter=' ')

# Data compiling and computation of the radial positions
mask=((data[:,0]-center[0])**2.0+(data[:,1]-center[1])**2.0<(radius)**2.0)*(data[:,2]<2000.0)*(data[:,3]<2000.0)
data=data[mask]
coordinates=np.zeros((np.shape(data)[0],6))     # Format: radial position, radius of the sphere, depth, width_x, width_y, width_x-width_y (nm)
coordinates[:,0]=np.sqrt((data[:,0]-center[0])**2.0+(data[:,1]-center[1])**2.0)
coordinates[:,1]=center[1]*1.0
coordinates[:,2]=radius-np.sqrt(radius**2.0-coordinates[:,0]**2.0)
coordinates[:,3]=data[:,2]*1.0
coordinates[:,4]=data[:,3]*1.0
coordinates[:,5]=data[:,2]-data[:,3]

# Averaging
abscissa=np.arange(0.0,depthrange)
averagedwidth=np.zeros((len(abscissa),3))
uncertainty=np.zeros((len(abscissa),3))
numberofmolecules=np.zeros(len(abscissa))
for k in np.arange(len(abscissa)):
    mask=(np.abs(coordinates[:,2]-abscissa[k])<averagingwidth/2.0)
    averagedwidth[k,0]=np.mean(coordinates[mask,3])
    averagedwidth[k,1]=np.mean(coordinates[mask,4])
    averagedwidth[k,2]=np.mean(coordinates[mask,5])
    uncertainty[k,0]=np.std(coordinates[mask,3])/np.sqrt(np.sum(mask))
    uncertainty[k,1]=np.std(coordinates[mask,4])/np.sqrt(np.sum(mask))
    uncertainty[k,2]=np.std(coordinates[mask,5])/np.sqrt(np.sum(mask))
    numberofmolecules[k]=np.sum(mask)
    
calibrationexport=np.zeros((len(abscissa),4))
calibrationexport[:,0]=abscissa*1.0
calibrationexport[:,1]=averagedwidth[:,0]*1.0
calibrationexport[:,2]=averagedwidth[:,1]*1.0
calibrationexport[:,3]=averagedwidth[:,2]*1.0
np.savetxt("Results_calibration_astigmatism.txt",calibrationexport,header='Format: depth // width_x // width_y // width_x - width_y (all values in nm)')

# Display
if display==1:
    plt.figure(u"Point cloud")
    plt.plot(coordinates[:,2],coordinates[:,5],'xr',label=r'$w_x-w_y$')
    plt.xlim(0,depthrange)
    plt.legend()
    plt.xlabel('Depth (nm)')
    plt.ylabel('PSF width (nm)')
    plt.show()
elif display==2:
    plt.figure(u"Averaged curve")
    plt.errorbar(abscissa,averagedwidth[:,0],uncertainty[:,0],color='green',lw=3.0,label=r'$w_x$')
    plt.errorbar(abscissa,averagedwidth[:,1],uncertainty[:,1],color='blue',lw=3.0,label=r'$w_y$')
    plt.errorbar(abscissa,averagedwidth[:,2],uncertainty[:,2],color='red',lw=3.0,label=r'$w_x-w_y$')
    plt.legend()
    plt.xlabel('Depth (nm)')
    plt.ylabel('PSF width (nm)')
    plt.show()
elif display==3:
    plt.figure(u"Number of molecules detected")
    plt.plot(abscissa,numberofmolecules,color='black',lw=3.0)
    plt.xlabel('Depth (nm)')
    plt.ylabel('Number of molecules detected')
    plt.show()

print('')
print('Done')
print('')
