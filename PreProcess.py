# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:39:12 2019

@author: Nathan Giha
email: giha@umich.edu

General script for reading in DAFCA data files
Uses Will Steinberger's DataLoader and GetWaveData functions to extract info
Optimized for high-volume, command line use

Input:
    Arg 1: Config file with list of paths to data
    Arg 2: Config file with processing options

Output:
    File with list-mode data for each data set, file contains header with information on processing parameters used
    
To call in command line:
    
    ex. python PreProcess.py datapath.config options.config
"""

import numpy as np
import time
import os
import os.path
import argparse
import configparser

from dataloader import DataLoader
from getwavedata import GetWaveData


###############################################################################
####################### Command line parser ###################################
###############################################################################


'''
# Take datapath and config file as inputs in command line
parser = argparse.ArgumentParser(description='Processes list-mode waveform files from DAFCA.')
parser.add_argument('datapath', metavar='datapath', type=str, 
                   help='The path from which all data will be loaded')
parser.add_argument('options', metavar='options', type=str, 
                   help='Processing options')

config = parser.parse_args()



###############################################################################
####################### Unpack configurations #################################
###############################################################################

datapathList = 'path.config'

with open(config.datapath) as datapathList:
    read_data = datapathList.read()
options = config.options




###############################################################################
###############################################################################
###############################################################################
'''

### Read in options file for configuring analysis settings ####################

options = 'C:\\Users\\giha\\Documents\\GetWaveData\\config.ini'

config = configparser.ConfigParser()
config.read(options)


'''
Why would I handle this myself when getwavedata already does it?
Instead adapt getwavedata function to take in all waves from all files
From config file, don't need:
    -datafile name (should be unused)
    -data directory (has to become input of function)
    -data mgmt section
    
    Should I run it for each datafile individually? I think that'll work.
    The many for loops shouldn't matter, as cycling through those should not be
    the bottleneck for this program



# Setup data info
# Directories
data_directory = config['Directories']['data_directory']
data_file_name = config['Directories']['data_file_name']
pywaves_directory = config['Directories']['pywaves_directory']
    
# Digitizer
dataFormatStr = config['Digitizer']['dataFormat']
nSamples = int(config['Digitizer']['samples_per_waveform'])
ns_per_sample = int(config['Digitizer']['ns_per_sample'])
number_of_bits = int(config['Digitizer']['number_of_bits'])
dynamic_range_volts = float(config['Digitizer']['dynamic_range_volts'])
polarity = int(config['Digitizer']['polarity'])
baselineOffset = int(config['Digitizer']['baseline_offset'])
nBaselineSamples = int(config['Digitizer']['baseline_samples'])
nCh = int(config['Digitizer']['number_of_channels'])
nWavesPerLoad = int(config['Data Management']['waves_per_load'])
nWaves = int(config['Data Management']['waves_per_folder']) # per folder
startFolder = int(config['Data Management']['start_folder'])
nFolders = int(config['Data Management']['number_of_folders'])
unevenFactor = int(config['Data Management']['uneven_factor'])
cfdFraction = float(config['Pulse Processing']['cfd_fraction'])
integralEnd = int(config['Pulse Processing']['integral_end'])
totalIntegralStart = int(config['Pulse Processing']['total_integral_start'])
tailIntegralStart = int(config['Pulse Processing']['tail_integral_start'])
applyCRRC4 = bool(int(config['Pulse Processing']['apply_crrc4']))
CRRC4Tau = float(config['Pulse Processing']['crrc4_shaping_time'])
'''



# Read in path config file
with open('C:\\Users\\giha\\Documents\\GetWaveData\\path.config') as datapathList:
    dataList = datapathList.read().splitlines()



# Get number of paths specified in config file
pathNum = len(dataList)


### Function for finding all data files in a path
### Input: Path
### Output: List of paths of all datafiles
def dataFind(path):
    ls = [os.path.join(root, filename)
    for root, dirs, files in sorted(os.walk(path))
    for filename in files
    if filename.endswith('.dat')]    
    ls = sorted(ls, key=lambda x: int(os.path.split( os.path.split(x)[0])[1]))
    return ls

#ls = sorted(dataList, key=lambda x: int(filter(str.isdigit, x)))
#ls = dataList.sort( key=lambda x: int(''.join(filter(str.isdigit, x))))


test = 0
# Iterate over 
for i in range(pathNum):
    path = dataList[i]
    test = dataFind(path)
    

























