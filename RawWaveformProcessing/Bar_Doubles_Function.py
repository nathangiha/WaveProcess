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
	#DCFD = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
	#Fulltime = np.zeros((len(Data_Structure[0]), int(Data_Structure[1]*len(files))))
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
		
		for wave in np.arange(0, Number_of_Waves, 1):
			Channel_Index = np.where(Data_Structure[0] == float(Waves[wave][0]))[0][0]
			
			PH[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][1]
			PI[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][2]
			#DCFD[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][3]
			#Fulltime[Channel_Index][int(Counter[Channel_Index])] = ((Waves[wave]['TimeTag'] + 
            #                                                       ((Waves[wave]['Extras'] & 0xFFFF0000)
            #                                                       << 15) + fileTimeGap*f))*ns_per_sample
			Tails[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][6]
			Totals[Channel_Index][int(Counter[Channel_Index])] = Waves[wave][7]
			
			Counter[Channel_Index]+=1
			
		print("Breakdown of waves per channel: ")
		print(Counter)
		print("\n")
		
	######
	
	return Counter, PH, PI, Tails, Totals#DCFD, Fulltime, Tails, Totals

	
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