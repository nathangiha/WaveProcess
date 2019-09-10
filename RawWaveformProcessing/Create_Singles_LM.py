# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 9:22:13 2019

@author: wmst
email: wmst@umich.edu
cell: 757-870-1490 
"""
##############################################
##############################################
##############################################


import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.colors import LogNorm
import time
from collections import Counter
from matplotlib import cm


##############################################
############ Parameters to change ############
##############################################


Data_File = "H328"

pywaves_directory = "C:/Users/Giha/Documents/GetWaveData/RawWaveformProcessing/"

#Path_to_Data = "D:/Backscatter_Experiment/"+Data_File+"/"
#Path_to_Data = "D:/TOF_7_1_System/"+Data_File+"/"
#Path_to_Data = "D:/7_Stilbene_1_LYSO/"+Data_File+"/"
#Path_to_Data = "D:/CeBr/CeBr3_4_18_2019/"+Data_File+"/"
#Path_to_Data = "D:/"+Data_File+"/"
#Path_to_Data = "D:/TOF_2019/TOF_2019/Coincidence/"+Data_File+"/"
#Path_to_Data = "D:/TOF_2019/TOF_2019/H2DPI_Cal/"+Data_File+"/"
#Path_to_Data = "D:/TOF_2019/TOF_2019/Stilbene_1in_Cal/"+Data_File+"/"
#Path_to_Data = "D:/Gamma_M/"+Data_File+"/"
#Path_to_Data = "D:/Transfer_SB_2/"+Data_File+"/"
#Path_to_Data = "D:/TOF_Experiment_90_Degrees/"+Data_File+"/"
#Path_to_Data = "C:/H2DPI/Levi_Testing/"+Data_File+"/"
Path_to_Data = "D:/Position_Calibration_Data_7_1/8_Pillar_LYSO/8_Pillar_LYSO/"+Data_File+"/"

Output_Data_Path = "C:/H2DPI/Calibration/7_Stilbene_1_LYSO/List_Mode_Data/Singles/"+Data_File+"/"

Name_for_File = Data_File+"_"

Output_Data = True


##############################################
##############################################
##############################################

Num_Samples = 500

ns_per_sample = 2
number_of_bits = 14
dynamic_range_volts = 2.0
nBaselineSamples = 50
F = 0.2
	
VperLSB = dynamic_range_volts/(2**number_of_bits)

					   #0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
total_integral_start = [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0] #channel value
tail_integral_start =  [30,  30,  30,  30,  30,  30,  30,  30,  8,   30,  30,  30,  30,  30,  30,  30] #channel value
integral_end =         [185, 185, 185, 185, 185, 185, 185, 185, 55,  185, 185, 185, 185, 185, 185, 185] #channel value

#total_integral_start = [0]
#tail_integral_start = [8]
#integral_end = [55]

Negative_Waves = [8] # Will treat these channels as negative pulses

##############################################
##############################################
##############################################


sys.path.extend([pywaves_directory])

from dataloader import DataLoader


##############################################
##############################################
##############################################

def Analyzing_Waves():
	
	print("\n")
	print("Data file to be analyzed: "+str(Data_File))
	print("\n")
	
	files = os.listdir(Path_to_Data)
	
	#if not os.mkdir(Output_Data_Path):
	#	os.mkdir(Output_Data_Path)
		
	if not os.path.exists(Output_Data_Path):
		os.makedirs(Output_Data_Path)
	
	for f in files:
	
		Data = DataLoader(Path_to_Data+str(f)+"/dataFile0.dat",DataLoader.DAFCA_DPP_MIXED,Num_Samples)
		
		print("Reading in Folder: "+str(f))
		print("Number of waves: "+str(Data.GetNumberOfWavesInFile()))
		print("\n")
	
		Number_of_Waves = Data.GetNumberOfWavesInFile()
		Waves = Data.LoadWaves(Number_of_Waves)
		
		##############################################
		############### Data Structure ###############
		##############################################
		### ('Channel',(np.int16,1))
		### ('PH',(np.float64,1))
		### ('PI',(np.float64,1))
		### ('DCFD',(np.float64,1))
		###	('Timetag',(np.int32,1))
		###	('Extras',(np.int32,1))
		### ('Tail',(np.float64,1))
		###	('Total',(np.float64,1))
		##############################################
		##############################################
		
		Data_Out = np.zeros((len(Waves),9))
		
		for wave in np.arange(0,len(Waves),1):
			
			#print(Waves[wave]['EventSize'])
			#print(Waves[wave]['Format'])
			#print(Waves[wave]['Channel'])
			#print(Waves[wave]['Baseline'])
			#print(Waves[wave]['ShortGate'])
			#print(Waves[wave]['LongGate'])
			#print(Waves[wave]['TimeTag'])
			#print(Waves[wave]['Extras'])
			#print(Waves[wave]['Samples'])
			#print("\n")
			
			Data_Out[wave][0] = Waves[wave]['Channel']
			
			Channel_Val = int(Waves[wave]['Channel'])
			
			Subtracted_Wave = BaselineSubtract(Waves[wave]['Samples'], nBaselineSamples)
			
			if Waves[wave]['Channel'] in Negative_Waves:
				#x = np.arange(0,Num_Samples,1)
				#plt.plot(x, Subtracted_Wave)
				#plt.show()
				#plt.close()
				
				Subtracted_Wave = Subtracted_Wave*(-1.0)
				
				#plt.plot(x, Subtracted_Wave)
				#plt.show()
				#plt.close()
				
				#print(Channel_Val)
				#print(tail_integral_start[Channel_Val])
			
			Max_index = np.argmax(Subtracted_Wave)
			#print(Max_index)
			
			#x = np.arange(0,Num_Samples,1)
			#plt.plot(x, Waves[wave]['Samples'])
			#plt.scatter(x[Max_index+tail_integral_start[Channel_Val]:Max_index+integral_end[Channel_Val]], Subtracted_Wave[Max_index+tail_integral_start[Channel_Val]:Max_index+integral_end[Channel_Val]])
			#plt.scatter(x[Max_index+total_integral_start[Channel_Val]:Max_index+integral_end[Channel_Val]], Subtracted_Wave[Max_index+total_integral_start[Channel_Val]:Max_index+integral_end[Channel_Val]])
			#plt.show()
			#plt.close()
			
			ph = np.max(Subtracted_Wave)*VperLSB
			PI = np.sum(Subtracted_Wave)*VperLSB*ns_per_sample
			
			Data_Out[wave][1] = ph
			Data_Out[wave][2] = PI
			
			DCFD = CFD(Subtracted_Wave, F)
			
			Data_Out[wave][3] = DCFD
			Data_Out[wave][4] = Waves[wave]['TimeTag']
			Data_Out[wave][5] = Waves[wave]['Extras']
			
			Tail = np.sum(Subtracted_Wave[Max_index+tail_integral_start[Channel_Val]:Max_index+integral_end[Channel_Val]])
			Total = np.sum(Subtracted_Wave[Max_index+total_integral_start[Channel_Val]:Max_index+integral_end[Channel_Val]])
			
			Data_Out[wave][6] = Tail
			Data_Out[wave][7] = Total
		
		Writing_Data(Data_Out, f)

##############################################
	
	
def BaselineSubtract(Wave, nBaselineSamples):
	baseline = np.average(Wave[:nBaselineSamples])
	blsSamples = Wave - baseline
	return blsSamples

	
##############################################
	
	
def CFD(Blnd_Wave, F):
	CFD_Val = F*max(Blnd_Wave)
	counter = np.argmax(Blnd_Wave) 
	
	while Blnd_Wave[counter] > CFD_Val:
		counter -= 1
	
	Time_Range = range(0,Num_Samples*2,2)
	y_2 = Blnd_Wave[counter+1]
	y_1 = Blnd_Wave[counter]
	y = CFD_Val
	x_1 = Time_Range[counter]
	x_2 = Time_Range[counter+1]
	
	
	Start_Time = x_1 + (y-y_1)*(x_2-x_1)/(y_2-y_1)
	
	return Start_Time

	
##############################################

	
def Writing_Data(Doubles_Data,f):
	
	##############################################
	############### Data Structure ###############
	##############################################
	### ('Channel',(np.int16,1))
	### ('PH',(np.float64,1))
	### ('PI',(np.float64,1))
	### ('DCFD',(np.float64,1))
	###	('Timetag',(np.int32,1))
	###	('Extras',(np.int32,1))
	### ('Tail',(np.float64,1))
	###	('Total',(np.float64,1))
	##############################################
	##############################################
	
	Dat_Out_File = Output_Data_Path+Name_for_File+f+"_"+str(F)+"_"+str(total_integral_start[0])+"_"+str(tail_integral_start[0])+"_"+str(integral_end[0])+".dat"
	Out = open(Dat_Out_File, "wb")
	
	Channel ='f0'
	PH = 'f1'
	PI = 'f2'
	DCFD = 'f3'
	Timetag = 'f4'
	Extras = 'f5'
	Tail = 'f6'
	Total = 'f7'
	
	outputStructure = np.zeros(len(Doubles_Data), dtype='int16, float64, float64, float64, int32, int32, float64, float64')
	
	for coincidence in np.arange(0,len(Doubles_Data),1):
		outputStructure[coincidence][Channel] = Doubles_Data[coincidence][0]
		outputStructure[coincidence][PH] = Doubles_Data[coincidence][1]
		outputStructure[coincidence][PI] = Doubles_Data[coincidence][2]
		outputStructure[coincidence][DCFD] = Doubles_Data[coincidence][3]
		outputStructure[coincidence][Timetag] = Doubles_Data[coincidence][4]
		outputStructure[coincidence][Extras] = Doubles_Data[coincidence][5]
		outputStructure[coincidence][Tail] = Doubles_Data[coincidence][6]
		outputStructure[coincidence][Total] = Doubles_Data[coincidence][7]
	
	outputStructure.tofile(Out)
	

##############################################

def Running():
	startTime = time.time()
	print("Running GetWaveData!")
	print("Starting at " + time.strftime('%H:%M:%S'))
	
	Analyzing_Waves()
	
	print("\n")
	print("Cave Johnson. We're done here.")

Running()