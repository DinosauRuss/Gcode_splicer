

'''
Program to combine 2 Slic3r generated gcode files with different
settings at specified z-axis height

All commands sent through command line
'''

import os
import re


# Don't overwrite previous file with same name
def checkNewName(newName):
    while os.path.isfile(newName):
        print(newName + ' already exists')
        newName = checkNewName(input('Enter a different name for new file: '))
        
    else:
        return newName


# Layer must exist in file
def verifyLayer(gcodeFile, layerHeight):
    with open(os.getcwd() + '/' + gcodeFile, 'r') as inFile:
        checkLayer = re.search(r'{}'.format(layerHeight), inFile.read())
        
    if checkLayer == None:
        print('Layer \'{}\' not found in \'{}\', please check files'
              .format(layerHeight, gcodeFile))
        return False
    else:
        return True


# Verify if files exist before continuing
def verifyFileName(fileName, whichFile):
    
    while not os.path.isfile(fileName):
        print('\n\'' + fileName + '\' is not a file in this directory')
        fileName = verifyFileName(input('Try Again\n\nEnter {} file: '.
                                    format(whichFile)), whichFile)
    else:
        return fileName

    
# Add every line from first file to new file, until desired layer height
def writeInitialFile(firstFile, newFile, layerHeight):
    
    with open(os.getcwd() + '/' + firstFile, 'r') as inFile:
        with open(newFile, 'w') as outFile:
            line = ''
            
            # read beginning of line, check for match to layer height variable
            while line[:len(layerHeight)] != layerHeight:
                line = inFile.readline()
                
                if line[:len(layerHeight)] == layerHeight:
                    outFile.write('\n; ----- End of First File -----\n\n')
                    break
                else:
                    outFile.write(line)


# Append every line from second file to new file, following desired
# layer height
def writeSecondHalfFile(secondFile, newFile, layerHeight):
    
    with open(os.getcwd() + '/' + secondFile, 'r') as inFile:
        with open(newFile, 'a') as outFile:
            line = ''
            
            # read beginning of line, check for match to layer height variable
            while line[:len(layerHeight)] != layerHeight:
                line = inFile.readline()
            
            outFile.write('\n; ----- Beginning of new file -----\n\n')
            while line != '':
                outFile.write(line)
                line = inFile.readline()



def mainLoop():
    
    # initial gcode file
    begFile = verifyFileName(input('Enter first file: '), 'First file')
    
    # second gcode file
    endFile = verifyFileName(input('Enter second file: '), 'Second file')
    
    newFileName = checkNewName(input('Enter name of file to create: '))
    
    whichLayer = 'G1 Z' + input('Enter layer height to split files: ')
    if verifyLayer(begFile, whichLayer) == False or \
        verifyLayer(endFile, whichLayer) == False:
        quit()
    
    
    writeInitialFile(begFile, newFileName, whichLayer)
    writeSecondHalfFile(endFile, newFileName, whichLayer)
    
    
    print('New gcode file \'{}\' is complete'.format(newFileName)) 
    
    
    

mainLoop()
                
        
        
