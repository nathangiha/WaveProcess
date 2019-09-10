# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:12:07 2019

@author: Giha

Plot glass and stilbene histograms, but make it fashion
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
#dataglass = GetWaveData("C:/Users/Giha/Documents/GetWaveData/configg.ini")
#datastil = GetWaveData("C:/Users/Giha/Documents/GetWaveData/configs.ini")

# Get pulse integrals
intglass = dataglass[1][1][:]
intstil = datastil[1][1][:]


# Histogram pulse integrals
binedges = np.arange(start = 0, stop = 30, step = 0.25)

histglass, temp = np.histogram(intglass, bins = binedges)
histstil, temp = np.histogram(intstil, bins = binedges)

# Normalize to time
measTime = 1800 # seconds
histglass = histglass / measTime
histstil = histstil / measTime

# Plot histograms
centers = (binedges[:-1]+binedges[1:])/2
width = binedges[1]-binedges[0]

plt.close()
plt.bar(centers, histglass, align='center', alpha = 0.75, width = width, label = 'glass')
plt.bar(centers, histstil, align='center', alpha = 0.75, width = width, label = 'stilbene')

plt.xlabel(r'Pulse Integral $(V-ns)$')
plt.ylabel(r'Count Rate $(s^{-1})$')
plt.legend()

plt.axis([0,30,0,1.5])

plt.show()
