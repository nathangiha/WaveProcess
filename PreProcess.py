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
import sys
import argparse

from dataloader import DataLoader
from getwavedata import GetWaveData


###############################################################################
####################### Command line parser ###################################
###############################################################################

parser = argparse.ArgumentParser(description='Process some integers.')


###############################################################################
####################### User Inputs ###########################################
###############################################################################







###############################################################################
###############################################################################
###############################################################################
