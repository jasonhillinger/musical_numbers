# Requires 
# vlc 64 bit already installed on computer
# pip install python-vlc
# python3 -m pip install mutagen    OR      sudo apt-get install python3-mutagen

# Description
# A robot is created which takes in an integer number and plays a note depending on the value
# Each input integer is transformed into binary and each bit will represent the on and off state of a note
# Every note is attempted to be played when activateBeep is called

import vlc
from time import sleep
from mutagen.mp3 import MP3
from os import listdir

# This is where the number set is stored to be played
import number_set

# Increase to increase the speed, Recommended to set to 1 or 2, maybe 3 for really fast
SPEED = 17

MP3_FOLDER = "piano-mp3"
print("Finding MP3 files...")
MP3_FILES_NAMES = listdir(MP3_FOLDER)


class RobotData:
    def __init__(self,DEBUG) -> None:
        self.DEBUG = DEBUG

        # initializing params to all 0
        self.params = []
        for i in range(len(MP3_FILES_NAMES)):
            self.params.append(0)
        self.printDebug("All MP3 files found!")

        # Loading MP3 files into paramsNotes list
        self.printDebug("LOADING MP3 FILES")
        self.paramsNotes = []
        for i in MP3_FILES_NAMES:
            path_to_file = MP3_FOLDER + "/" + i
            self.printDebug(path_to_file)
            self.paramsNotes.append((vlc.MediaPlayer(path_to_file), MP3(path_to_file).info.length / SPEED))
        self.printDebug("MP3 FILES LOADED")
        
        # This variable stores the binary version of the number before being split into a list
        self._paramsBufferValue = bin(0)

    def print(self) -> None:
        print(self.params)

    def printDebug(self,message) -> None:
        if self.DEBUG:
            print(message)

    def setDebug(self, val) -> None:
        self.DEBUG = val
        print("DEBUG SET TO " + str(val).upper())

    def receiveData(self, data) -> bool:
        # TODO change max size to the size of an 89 digit number
        if data < 0:
            self.printDebug("DATA OUT OF RANGE")
            return False
        
        # Params is a 8 bit number, removes the 0b prefix, fills unused bits with zeros (zfill)
        self._paramsBufferValue = bin(data)[2:].zfill(len(self.params))
        return True

    def setParams(self) -> bool:
        # TODO check size of params ?
        for i in range(len(self._paramsBufferValue)):
            self.params[i] = int(self._paramsBufferValue[i]) 
        return True
        
    
    def activateSound(self) -> None:
        for i in range(len(self.params)):
            if self.params[i] == 1:
                self.paramsNotes[i][0].play()
                self.printDebug("WAITING : " + str(self.paramsNotes[i][1]) + " seconds" )
                sleep(self.paramsNotes[i][1])
                self.paramsNotes[i][0].stop()
        return


# Initializing Robot with debug set to false
rob = RobotData(False)

print("Playing your number set!")
for i in number_set.NUMBER_SET:
    print("Number: " + str(i))
    if( rob.receiveData(i) ):
        rob.setParams()
        rob.activateSound()
