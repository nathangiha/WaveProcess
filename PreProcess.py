# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:39:12 2019

@author: Nathan Giha
email: giha@umich.edu

General script for reading in DAFCA data files
Uses Marc Ruch's DataLoader and a modified GetWaveData to extract info
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
from getwavedataRefitted import GetWaveDataR


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
datapathList = 'path.config'



'''
From config file, don't need:
    -datafile name (should be unused)
    -data directory (has to become input of function)
    -data mgmt section
    
    9/10
    Should I run it for each datafile individually? I think that'll work.
    The many for loops shouldn't matter, as cycling through those should not be
    the bottleneck for this program
    
    9/11
    Nah, this dumb af. The dataFind function is still useful, just use it to
    find the number of folders and then feed that to GetWaveData


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
# Iterate over paths
for n in range(pathNum):
    # Get path
    path = dataList[n]
    
    # Get list of datafiles in path, then find number of files
    fileList = dataFind(path)
    
    # Feed options.config, data directory, and number of files to GetWaveDataR
    data = GetWaveDataR(options, path, fileNum =len(fileList) )
    test = data
    
    
    
    
    
    
    
        
    





