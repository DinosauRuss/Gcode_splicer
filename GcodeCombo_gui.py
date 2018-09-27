

'''
GUI program to combine 2 Slic3r generated gcode files with different
settings at specified z-axis height 
'''

import os
import re
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *


########## Functions ########## 

def checkNewName(newName):
    'Don\'t overwrite previous file with same name'
    
    while os.path.isfile(newName):
        print(newName + ' already exists')
        newName = checkNewName(input('Enter a different name for new file: '))
        
    else:
        return newName


def verifyLayer(gcodeFile, layerHeight):
    'Layer must exist in file'
    
    with open(gcodeFile, 'r') as inFile:
        checkLayer = re.search(r'{}'.format(layerHeight), inFile.read())
        
    if checkLayer == None:
        #~ print('Layer \'{}\' not found in \'{}\', please check files'
              #~ .format(layerHeight, gcodeFile))
        messagebox.showerror('Layer Error', 'Layer \'{}\' not found in:\
            \n\n\'{}\'\n\nplease check files'.format(layerHeight, gcodeFile))
        return False
    else:
        return True


def verifyFileName(filename, whichFile):
    'Verify if files exist before continuing'
    
    while not os.path.isfile(filename):
        messagebox.showerror('Error', '{} is not valid'.format(whichFile))
        return False
    else:
        return filename


def writeInitialFile(firstFile, newFile, layerHeight):
    'Add every line from first file to new file, until desired layer height'
    
    with open(firstFile, 'r') as inFile:
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


def writeSecondHalfFile(secondFile, newFile, layerHeight):
    'Append every line from second file to new file, following desired\
     layer height'
     
    with open(secondFile, 'r') as inFile:
        with open(newFile, 'a') as outFile:
            line = ''
            
            # read beginning of line, check for match to layer height variable
            while line[:len(layerHeight)] != layerHeight:
                line = inFile.readline()
            
            outFile.write('\n; ----- Beginning of new file -----\n\n')
            while line != '':
                outFile.write(line)
                line = inFile.readline()


def compute():
    'Check all information and generate/save new file'
    
    while True:
        # initial gcode file
        begFile = verifyFileName(file_1_disp_var.get(), 'Beginning file')
        # second gcode file
        endFile = verifyFileName(file_2_disp_var.get(), 'Ending file')
        
        # Break out of 'compute' callback if either file bad
        if begFile == False or endFile == False:
            break
        
        # Layer height must be float
        try:
            float(layer_entry.get())
        except:
            messagebox.showinfo('Error', 'Layer Height must be a number, in mm')
            break
            
        whichLayer = 'G1 Z' + str(layer_entry.get())
        if verifyLayer(begFile, whichLayer) == False or \
            verifyLayer(endFile, whichLayer) == False:
            break
        
        newFileName = asksaveasfilename(defaultextension='.gcode',\
            title='Save new gcode file', confirmoverwrite=True)
        print(newFileName)
        
        # Escape 'compute' if save canceled
        if newFileName:
            writeInitialFile(begFile, newFileName, whichLayer)
            writeSecondHalfFile(endFile, newFileName, whichLayer)
        else:
            break
        
        messagebox.showinfo('Complete', 'New gcode file is complete')
        
        # Reset field variables
        file_1_disp_var.set('')
        file_2_disp_var.set('')

        break 


########## GUI Control ##########

main = Tk() # Main tk GUI object
main.title('Gcode Adjuster')
main.resizable(False, False)
#~ main.geometry('400x300')

menubar = Menu(main)    # Menubar for top of window
main.config(menu=menubar)   # display the menubar

# 'File' dropdown
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Quit', command=lambda: quit())

# 'About' dropdown
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label='About', \
    command=lambda: messagebox.showinfo('About', 'Written by REK'))

# Add dropdowns to main menubar
menubar.add_cascade(label='File', menu=filemenu)  
menubar.add_cascade(label='Help', menu=aboutmenu)


# Variables
file_1_disp_var = StringVar()   # Variable to display file 1 location
file_2_disp_var = StringVar()   # To display file 2 location


# Single frame to put all elements in
mainframe = Frame(main)
mainframe.grid(padx=15, pady=15)


# Left side
file_1 = Label(mainframe, text='First file: ', width=13, anchor=W)
file_1.grid()

file_2 = Label(mainframe, text='Second file: ', width=13, anchor=W)
file_2.grid()

layer = Label(mainframe, text='Layer height: ', width=13, anchor=W)
layer.grid()


# Center
file_1_disp = Label(mainframe, width=40, anchor=W, textvariable=file_1_disp_var)
file_1_disp.grid(column=1, row=0)
    
file_2_disp = Label(mainframe, width=40, anchor=W, textvariable=file_2_disp_var)
file_2_disp.grid(column=1, row=1)

layer_entry = Entry(mainframe, width=7, bg='white')
layer_entry.grid(column=1, row=2, sticky=W)


# Right side
file_1_b = Button(mainframe, text='Select file', width=10,\
    command=lambda: file_1_disp_var.set(askopenfilename()))
file_1_b.grid(column=2, row=0)

file_2_b = Button(mainframe, text='Select file', width=10,\
    command=lambda:file_2_disp_var.set(askopenfilename()))
file_2_b.grid(column=2, row=1)

compute = Button(mainframe, text='Compute\nand save', width=10,\
    command=compute, height=3, bg='lightskyblue')
compute.grid(column=2, row=3)




########## Main Program ##########

main.mainloop()
    
    
    
    
     
        
        
