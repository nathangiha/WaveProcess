# -*- coding: utf-8 -*-
"""
Created on Tue Apr 9 10:51:13 2019

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


Data_File = "H387"

#H387 - Strong Cf-252 - 20"
#H401 - Strong Cf-252

pywaves_directory = "C:/H2DPI/Calibration/7_Stilbene_1_LYSO/Backscatter/Processing_Scripts/"

Path_to_Data = "C:/H2DPI/Calibration/7_Stilbene_1_LYSO/List_Mode_Data/Singles/"+Data_File+"/"

Output_Data = True

Output_Path = "C:/H2DPI/Calibration/7_Stilbene_1_LYSO/List_Mode_Data/Doubles/"

if Output_Data:
	Out = open(Output_Path+Data_File+"_Neutron_Doubles.dat","wb")

Max_Time_Window = 30 #ns 
Min_Time_Window = 0 #ns

Stilbene_Channels = [0,2,4,6,10,12,14]
Stilbene_Channels = [0,1,2,3,4,5,6]
Bars = [0,1,2,3,5,6,7]

LYSO_Chan = [8]

Number_Bars = 8
Number_Channels = 14

##############################################
##############################################
##############################################


fileTimeGap = 2**43 # Note: no more than 3 hours per measurement!
ns_per_sample = 2

sys.path.extend([pywaves_directory])

from readsingles import ReadSingles


Time_Offset = np.array([0.0, # Channels 0,1 ; Bar 1
						0.0, # Channels 2,3 ; Bar 2
						0.0, # Channels 4,5 ; Bar 3
						0.0, # Channels 6,7 ; Bar 4
						0.0, # Channels 8,9 ; Bar 5
						0.0, # Channels 10,11 ; Bar 6
						8.0, # Channels 12,13 ; Bar 7
						8.0])# Channels 14,15 ; Bar 8

##############################################
##############################################
##############################################


def Analyzing_Waves():
	
	List_Data = Bars_Doubles(Path_to_Data)
	
	Counter = np.zeros(Number_Bars)
	
	PH = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	PI = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	Z_Ratio = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	DCFD = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	Fulltime = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	Start_Time = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	Tails = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	Totals = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	PSD_Ratios = np.zeros((Number_Bars, int(np.max(List_Data[0]))))
	
	for chan in np.arange(0, Number_Channels, 2):
		Num_Events = int(List_Data[0][chan])
		Counter[int(chan/2.0)] = Num_Events
		Bar = Bars[int(chan/2.0)]
		PH[int(chan/2.0)][:Num_Events] = List_Data[1][chan][:Num_Events] + List_Data[1][chan+1][:Num_Events]
		PI[int(chan/2.0)][:Num_Events] = List_Data[2][chan][:Num_Events] + List_Data[2][chan+1][:Num_Events]
		Z_Ratio[int(chan/2.0)][:Num_Events] = List_Data[2][chan][:Num_Events]/(List_Data[2][chan][:Num_Events] + List_Data[2][chan+1][:Num_Events])
		DCFD[int(chan/2.0)][:Num_Events] = (List_Data[3][chan][:Num_Events] + List_Data[3][chan+1][:Num_Events])/2.0
		Fulltime[int(chan/2.0)][:Num_Events] = (List_Data[4][chan][:Num_Events] + List_Data[4][chan+1][:Num_Events])/2.0 + Time_Offset[Bar]
		Start_Time[int(chan/2.0)][:Num_Events] = DCFD[int(chan/2.0)][:Num_Events] + Fulltime[int(chan/2.0)][:Num_Events]
		Tails[int(chan/2.0)][:Num_Events] = np.sqrt(List_Data[5][chan][:Num_Events]**2 + List_Data[5][chan+1][:Num_Events]**2)
		Totals[int(chan/2.0)][:Num_Events] = np.sqrt(List_Data[6][chan][:Num_Events]**2 + List_Data[6][chan+1][:Num_Events]**2)
		PSD_Ratios[int(chan/2.0)][:Num_Events] = Tails[int(chan/2.0)][:Num_Events]/Totals[int(chan/2.0)][:Num_Events]
		
	#####
		
	All_Times = []
	for start_times in Start_Time:
		All_Times = All_Times + start_times.tolist()
	All_Times.sort()
	
	Coincident_Events = Finding_Coincident_Events(All_Times, Min_Time_Window, Max_Time_Window)
	
	#####
	
	Counter_Data_Out = 0
	Coincident_Data_Out = np.zeros((len(Coincident_Events), 12))
	
	#####
	
	for coincidence in np.arange(0,len(Coincident_Events),1):
		
		First_Index = np.where(Start_Time == Coincident_Events[coincidence][0])
		First_Bar = First_Index[0][0]
		First_Bar = Bars[First_Index[0][0]]
		First_Place = First_Index[1][0]
		
		Second_Index = np.where(Start_Time == Coincident_Events[coincidence][1])
		Second_Bar = Second_Index[0][0]
		Second_Bar = Bars[Second_Index[0][0]]
		Second_Place = Second_Index[1][0]
		
		if int(First_Bar) in (Bars) and int(Second_Bar) in (Bars): 
			#print(First_Bar)
			#print(Second_Bar)
			Delta_DCFD = DCFD[Second_Bar][Second_Place] - DCFD[First_Bar][First_Place]
			Delta_Fulltime = Fulltime[Second_Bar][Second_Place] - Fulltime[First_Bar][First_Place]
			
			Coincident_Data_Out[Counter_Data_Out][0] =  First_Bar                            # Stilbene Bar number
			Coincident_Data_Out[Counter_Data_Out][1] =  Second_Bar                           # LYSO Bar Number
			Coincident_Data_Out[Counter_Data_Out][2] =  PH[First_Bar][First_Place]           # Stilbene PH
			Coincident_Data_Out[Counter_Data_Out][3] =  PH[Second_Bar][Second_Place]         # LYSO PH
			Coincident_Data_Out[Counter_Data_Out][4] =  PI[First_Bar][First_Place]           # Stilbene PI
			Coincident_Data_Out[Counter_Data_Out][5] =  PI[Second_Bar][Second_Place]         # LYSO PI
			
			Coincident_Data_Out[Counter_Data_Out][6] =  Delta_DCFD                           # DCFD Difference 
			Coincident_Data_Out[Counter_Data_Out][7] =  Delta_Fulltime                       # Full time Difference 
			
			Coincident_Data_Out[Counter_Data_Out][8] =  Z_Ratio[First_Bar][First_Place]      # Z Ratio for Stilbene
			Coincident_Data_Out[Counter_Data_Out][9] =  Z_Ratio[Second_Bar][Second_Place]    # Z Ratio for LYSO
			
			Coincident_Data_Out[Counter_Data_Out][10] = PSD_Ratios[First_Bar][First_Place]   # PSD Ratio for stilbene
			Coincident_Data_Out[Counter_Data_Out][11] = PSD_Ratios[Second_Bar][Second_Place]   # PSD Ratio for stilbene
			
			#print(Coincident_Data_Out[Counter_Data_Out])
			
			Counter_Data_Out+=1
		
	#####
	
	print("\n")
	print("Number of Coincident Events: "+str(Counter_Data_Out))
	print("\n")
	
	#####
	
	if Output_Data:
		
		print("\n")
		print("Writing Coincident Events to File")
		print("\n")
		
		Writing_Data(Coincident_Data_Out[:Counter_Data_Out])
	
##############################################


def Number_of_Channels(Path_to_Data, file):
	Data = ReadSingles(Path_to_Data+file)
	Number_of_Waves = Data.GetNumberOfWavesInFile()
	Waves = Data.LoadWaves(Number_of_Waves)
	
	Channels = np.zeros(Number_of_Waves)
	
	for wave in np.arange(0,Number_of_Waves,1):
		Channels[wave] = Waves[wave][0]
	
	Channels_Specified = np.array(list(set(Channels)))
	
	return Channels_Specified, Number_of_Waves

	
##############################################


def Bars_Doubles(Path_to_Data):
	
	files = os.listdir(Path_to_Data)
	
	Data_Structure = Number_of_Channels(Path_to_Data, files[0])
	
	print("Channels being read in: ")
	for ch in Data_Structure[0]:
		print("Channel: "+str(ch))
	print("\n")
	
	Counter=np.zeros(len(Data_Structure[0]))
	
	PH = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
	PI = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
	DCFD = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
	Fulltime = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
	Tails = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
	Totals = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
	
	######
	
	for f in np.arange(1,len(files)+1,1):
		
		Data = ReadSingles(Path_to_Data+files[f-1])
		
		print("Reading in File: "+str(files[f-1]))
		print("Number of Data Structures: "+str(Data.GetNumberOfWavesInFile()))
		print("\n")
		
		Number_of_Waves = Data.GetNumberOfWavesInFile()
		Waves = Data.LoadWaves(Number_of_Waves)
		
		Counter=np.zeros(len(Data_Structure[0]))
		
		for wave in np.arange(0, Number_of_Waves, 1):
			Channel_Index = np.where(Data_Structure[0] == float(Waves[wave][0]))[0][0]
			
			PH[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][1]
			PI[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][2]
			DCFD[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][3]
			Fulltime[Channel_Index][int(Counter[Channel_Index])] = ((Waves[wave]['TimeTag'] + 
                                                                   ((Waves[wave]['Extras'] & 0xFFFF0000)
                                                                   << 15) + fileTimeGap*f))*ns_per_sample
			Tails[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][6]
			Totals[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][7]
			
			Counter[Channel_Index]+=1
			
		print("Breakdown of waves per channel: ")
		print(Counter)
		print("\n")
		
	######
	
	return Counter, PH, PI, DCFD, Fulltime, Tails, Totals
	
	
##############################################


def Finding_Coincident_Events(All_Times, Min_Time_Window_Bar, Max_Time_Window_Bar):
	
	Coincidences = []
	Coincidence_Doubles = []
	Coincidence_Triples = []
	
	Data_Counter = 0 
	
	while Data_Counter < len(All_Times)-2:
		First = All_Times[Data_Counter]
		Second = All_Times[Data_Counter+1]
		Third = All_Times[Data_Counter+2]
		
		if First == 0:
			Data_Counter+=1
		else:
			First_Diff = Second - First
			Second_Diff = Third - First
			
			if Second_Diff < Max_Time_Window_Bar and Second_Diff > Min_Time_Window_Bar:
				Coincidence = [First, Second, Third]
				Coincidence_Triples.append(Coincidence)
				#Coincidences.append(Coincidence)
				Data_Counter+=3
			elif First_Diff < Max_Time_Window_Bar and First_Diff > Min_Time_Window_Bar:
				Coincidence = [First, Second]
				Coincidence_Doubles.append(Coincidence)
				Coincidences.append(Coincidence)
				Data_Counter+=2
			else:
				Data_Counter+=1
	
	print("\n")
	print("Number of Double Events: "+str(len(Coincidence_Doubles)))
	print("Number of Triple Events: "+str(len(Coincidence_Triples)))
	print("Total Number of Coincident Events: "+str(len(Coincidences)))
	print("\n")
	return Coincidences


##############################################

	
def Writing_Data(Doubles_Data):
	
	##############################################
	############### Data Structure ###############
	##############################################
	### ('Stilbene Bar number',(np.int16,1))
	### ('LYSO Bar number',(np.int16,1))
	### ('PH S',(np.float64,1))
	### ('PH L',(np.float64,1))
	### ('PI S',(np.float64,1))
	### ('PI L',(np.float64,1))
	### ('Delta DCFD',(np.float64,1))
	###	('Delta FT',(np.float64,1))
	###	('Z Ratio S',(np.float64,1))
	### ('Z Ratio L',(np.float64,1))
	###	('PSD Ratio S',(np.float64,1))
	##############################################
	##############################################
	
	Bar_1 ='f0'
	Bar_2 ='f1'
	PI_1 = 'f2'
	PI_2 = 'f3'
	D_DCFD = 'f4'
	D_FT = 'f5'
	Z_1 = 'f6'
	Z_2 = 'f7'
	PSD_1 ='f8'
	PSD_2 ='f9'
	
	outputStructure = np.zeros(len(Doubles_Data), dtype='int16, int16, float64, float64, float64, float64, float64, float64, float64, float64')
	
	for coincidence in np.arange(0,len(Doubles_Data),1):
		outputStructure[coincidence][Bar_1] = Doubles_Data[coincidence][0]
		outputStructure[coincidence][Bar_2] = Doubles_Data[coincidence][1]
		outputStructure[coincidence][PI_1] = Doubles_Data[coincidence][4]
		outputStructure[coincidence][PI_2] = Doubles_Data[coincidence][5]
		outputStructure[coincidence][D_DCFD] = Doubles_Data[coincidence][6]
		outputStructure[coincidence][D_FT] = Doubles_Data[coincidence][7]	
		outputStructure[coincidence][Z_1] = Doubles_Data[coincidence][8]
		outputStructure[coincidence][Z_2] = Doubles_Data[coincidence][9]
		outputStructure[coincidence][PSD_1] = Doubles_Data[coincidence][10]
		outputStructure[coincidence][PSD_2] = Doubles_Data[coincidence][11]
	
	outputStructure.tofile(Out)

	
##############################################

##############################################
##############################################
##############################################


def Running():
	startTime = time.time()
	print("Running GetWaveData!")
	print("Starting at " + time.strftime('%H:%M:%S'))
	
	Analyzing_Waves()
	
	endTime = time.time()
	runTime = endTime - startTime
	print("Find_Doubles took {} s".format(runTime))
	
	print("\n")
	print("Cave Johnson. We're done here.")

Running()