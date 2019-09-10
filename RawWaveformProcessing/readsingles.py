import numpy as np
import os

class ReadSingles:
    def __init__(self, fileName):#num Samples is the number of samples in a waveform, not number of waves
        self.fileName = fileName

        self.blockType = np.dtype([('Channel',(np.int16,1)),
                                   ('PH',(np.float64,1)),
                                   ('PI',(np.float64,1)),
                                   ('DCFD',(np.float64,1)),
                                   ('TimeTag',(np.int32,1)),
                                   ('Extras',(np.int32,1)),
                                   ('Tail',(np.float64,1)),
                                   ('Total',(np.float64,1))])
        
        self.location = 0
    
    def GetNumberOfWavesInFile(self):
        return int(os.path.getsize(self.fileName) / self.blockType.itemsize)
        
    def LoadWaves(self, numWaves):
        """Loads numWaves waveforms. If numWaves == -1, loads all waveforms in the file"""
        fid = open(self.fileName, "rb")
        fid.seek(self.location, os.SEEK_SET)
        self.location += self.blockType.itemsize * numWaves
        return np.fromfile(fid, dtype = self.blockType, count=numWaves)
    
    def Rewind(self):
        self.location = 0

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