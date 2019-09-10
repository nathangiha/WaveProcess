# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:37:29 2019

@author: Giha

Plot glass timing histogram, using 2-channel Na-22 singles data and
Cs-137 calibration data
"""

# Libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.colors import LogNorm
from scipy.special import erf
import time
from scipy.optimize import leastsq
import scipy
from scipy.optimize import curve_fit

from dataloader import DataLoader
from getwavedata import GetWaveData


# Import data and analyze with GetWaveData
#data = GetWaveData("C:/Users/Giha/Documents/GetWaveData/configg.ini")
#datastil = GetWaveData("C:/Users/Giha/Documents/GetWaveData/configs.ini")
dataNa = chNa
dataCs = chCs

# Get index of real pulses
rNa0 = np.nonzero(dataNa[8][0][:])
rNa1 = np.nonzero(dataNa[8][1][:])

# Make channel tags
ch0 = np.zeros(np.size(rNa0))
ch1 = np.ones (np.size(rNa1)) / 2

# Optain time tags and cfd, tag with channel number
ttt0 = dataNa[8][0][rNa0]
ttt1 = dataNa[8][1][rNa1]

cfd0 = dataNa[5][0][rNa0]
cfd1 = dataNa[5][1][rNa1]

# Clumsily concatenate data vectors with appropriate channel tags
ttt0 = np.vstack((ttt0,ch0)).T
ttt1 = np.vstack((ttt1,ch1)).T

cfd0 = np.vstack((cfd0,ch0)).T
cfd1 = np.vstack((cfd1,ch1)).T

# Concatenate channel times and add (assumes low coincidence rate in same detector)
ttt = np.append(ttt0,ttt1, axis=0)
cfd = np.append(cfd0,cfd1, axis=0)
t_tot = np.add(ttt,cfd)

# Sort, keeping channel tags intact
timeSort = t_tot[t_tot[:,0].argsort()]
tdiff = np.diff(timeSort, axis=0)

# Multiply time diff by channel diff, removing any same-detector coincidences and properly
# accounting for sequencing

tme = np.multiply(tdiff[:,0], tdiff[:,1])
tme = tme[np.nonzero(tme)]

# Plot histograms

# Histogram time bins
binedges = np.arange(start = -10, stop = 10, step = 0.1)

timeHist, temp = np.histogram(tme, bins = binedges)

# Normalize to time
measTime = 1800 # seconds
timeHist = timeHist / measTime

# Plot histograms
centers = (binedges[:-1]+binedges[1:])/2
width = binedges[1]-binedges[0]

plt.close()
plt.bar(centers, timeHist, align='center', alpha = 0.75, width = width, label = 'glass')

plt.xlabel(r'$\Delta t$')
plt.ylabel(r'Count Rate $(s^{-1})$')

plt.axis([-2.5,2.5,0,10])

plt.show()

# Fit Gaussian
mean = sum(centers*timeHist)/len(centers)
sigma = sum(timeHist*(centers-mean)**2)/len(centers)
def gaussian(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
popt, pcov = curve_fit(gaussian, centers, timeHist, p0 = [1, mean, sigma])
x = np.arange(-5,5,0.01)
plt.plot( x, gaussian(x, *popt), 'r-',label='Gaussian fit, FWHM = 318 ps')

plt.legend()
