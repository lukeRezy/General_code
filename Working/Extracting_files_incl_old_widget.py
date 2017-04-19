

'''
Luke Reisima
Version 2

Current version date:
16/04/2017

File contains:
1. Finding the Zip directory (anywhere),
2. prompting user for which directory(s) to use
3. Un-zipping into a tmp file
4. reading data out of the .tmp file into the .lmt structure
5. deleting the .tmp file

- Parent --> none
- Child --> read_LMT_data_in

Reliant on:
- See Importing section

Code Explanation:
- working on it
Otherwise ask Luke - 0278645084

Date Fully functional:
--- not yet ---

Work to complete:
- Retain some sort of 'default' directory if we are running the programe multiple times?
- at the moment its pretty quick to select which directories though.
- probably a "default" or "search" prompt would be useful?
- also just the normal uptade the Event structure to be a dict not a list.

'''

#-------------------------------------------------------------------------------#
# IMPORTING LIBRARIES AND FUNCTIONS
#-------------------------------------------------------------------------------#


# handling file structure and zipping
import glob, os.path, zipfile, tempfile, shutil

# impliments wait funcitons
import time

# XML data handling
import read_LMT_data_in as store_LMT

# XML file handling library
import xml.etree.ElementTree as ET

# .LMT data structure
import LMT_data_struct

import Directory_select

# this is for the basic gui
from tkinter import *
import tkinter


#-------------------------------------------------------------------------------#
# Globals
#-------------------------------------------------------------------------------#


# Event is the broadest data structure, it contains one run time worth of VSAT points
# Probably don't want this here long term
Event = LMT_data_struct.VSAT_out()


#-------------------------------------------------------------------------------#
# FUNCTIONS
#-------------------------------------------------------------------------------#


def handle_data(file_name, num_events):
    
    '''
    Handle_data takes the .tmp file name as the VSAT data container,
    It will iterate through the files until it finds the lmt.XML files
    then it will take the file path of that file and hand it to
    the data handling module "read_LMT_data_in".
    '''
    
    
    # Changes the directory to the appropriate .tmp folder
    os.chdir(file_name)
    
    # Assuming the initial .XML file is useless (it should be) we skip it and start at 201
    num = 201
    extn = "-lmt.xml"
    
    # This jumble of nested for loops is just getting through the file structure
    # to find the lmt.XML files
    
    for f in os.walk(file_name):
        for kk in f:
            for jj in kk:
                
                # the first lmt.XML file has a prefix "vb" rather than "vt"
                # which will not play nice, so we ignore it
                if ("lmt.xml" in jj) and not ("vb" in jj):
                    
                    # This is creating the "prefix" for the lmt.XML file
                    # Ie this would look like:
                    # "vt2017_03_10_00_01_06_ndt_p0_"
                    vsat_contg = '_'.join(jj.split("_")[:-1]) + "_"
                    
                    # this is where we are assuming there are only 8 .LMT files
                    while num < 1010:
                        
                        # This is putting the name of the lmt file back together
                        # Ie would look like:
                        # "vt2017_03_10_00_01_06_ndt_p0_" + "201" + "-lmt.xml"
                        tree = ET.parse(vsat_contg + str(num) + extn)
                        
                        # This is for the XML handler
                        root = tree.getroot()
                        
                        # Passes the data into the XML handler module
                        store_LMT.read_into_struct(root,num_events,Event)
                        
                        # Moves to the next lmt file
                        num += 101
                        
def check_dir(all_dir):
    
    #OBSOLETE NOW
    
    '''
    check_dir is the new addition and (after searching all directories) asks 
    the user for which directories to keep searching. Once selected the programe 
    will continue to check the selected directories for new .ZIP files
    '''
    
    # top is the "root" of the Gui
    top = tkinter.Tk()
    
    # Count is the key of the dictionary, which is also the index for the lsit of
    # directories, it pulls double duty
    count = 0
    
    # Rather than dynamically creating variable names, the dictionary holds them
    # together with the key as the same index as the list of directories. Therefore
    # if a directory is selected to be monitored, the key is used as the index to the list
    directories = {}
    go_to_dirs = []
    
    # iterates though ALL directories containing VSAT related data
    for one_dir in all_dir:
        
        # creates the tkinter object IntVar which holds the result of the check boxes
        # as noted the key to these is the same as the index of the directory in the list
        directories[count] = IntVar()
        
        # creates the check box object inside the tkinter "top" window
        C1 = Checkbutton(top, text = all_dir[count], variable = directories.get(count), \
                         onvalue = 1, offvalue = 0, height=1, \
                         width = 100)
        
        # puts the check box into the window
        C1.pack()
        count+=1
    
    # Brings the window to the front of the screen
    top.lift()
    top.attributes('-topmost',True)
    top.after_idle(top.attributes,'-topmost',False)
    top.mainloop()

    # checks which directorys have been selected to be monitored
    for key in directories.items():
        if key[1].get() == 1:
            
            # create a list of the directories to be monitored
            go_to_dirs.append(all_dir[key[0]])
            
    # returns the above list to main
    top.destroy()
    return go_to_dirs
                        

def get_dir():
    
    '''
    get_dir does the search for any VSAT related .ZIP files over the entire
    mac OS directory. This will need to be adjusted for windows
    It passes the list of file directorys back to main if A NEW .ZIP file is found
    '''
    
    all_dir = []
    
    # /Users is the highest level in the mac OS
    # os.walk() allows iteration though the file system
    for root, _, files in os.walk("/Users"):
        for f in files:
            fullpath = os.path.join(root, f)
            
            # checking if the file name holds a VSAT related suffix
            # and ignoring unrelated directories by SPECIFIC exemption
            if ("NDT_P0.ZIP" in fullpath):
                
                # checks to see if the specific .ZIP file has been handled already
                # this is assuming ALL .ZIP names are unique
                if ('/'.join(fullpath.split("/")[:-1])) not in all_dir:
                    all_dir.append(('/'.join(fullpath.split("/")[:-1])))
                
    return all_dir
                

def get_files(current_dir, files_done, num_events):
    
    '''
    get_files short cuts the search time down by looking only at user
    specified directories. Current_dir is one of the directories containing
    VSAT .ZIP files as already selected by the user. 
    
    This is basically a duplicate of the above search mechanism, but is much
    more targeted
    '''
    
    fuck_this = len(files_done)
    
    for root, _, files in os.walk(current_dir):
        for f in files:
            fullpath = os.path.join(root, f)
            
            # checking if the file name holds a VSAT related suffix
            # and ignoring unrelated directories by SPECIFIC exemption
            if ("NDT_P0.ZIP" in fullpath):
                
                # Checking for if the .ZIP file has already been targeted
                if fullpath.split("/")[-1] not in files_done:
                    # Create a new VSAT run event for a new .ZIP file
                    Event.add_event()
                    
                    # Create a temporary file to unzip into
                    tmp_dir = root + " tmp"
                    os.makedirs(tmp_dir)
                    
                    # Extract file to dir
                    zip_ref = zipfile.ZipFile(fullpath)
                    zip_ref.extractall(tmp_dir)
                    
                    # Pass the tmp file directory to the .lmt file handler (above)
                    # Ie would look like: /Users/Luke/Documents/2017/ENEL 400/Code/Transpower_2017_FYP/Reading .lmt files tmp
                    handle_data(('/'.join(fullpath.split("/")[:-2])) + "/" + tmp_dir.split("/")[-1], num_events)
                    
                    # Close the .ZIP
                    zip_ref.close()
                    
                    # Remove the temporary file
                    shutil.rmtree(root + " tmp", ignore_errors=True)
                    
                    # Returns the file path of the handled .ZIP
                    files_done.append( fullpath.split("/")[-1] )
                    
                    # this increases the number of VSAT events  by one
                    # it is handled buy increaseing the number of events 
                    # back inside main as well so we don't get duplicates
                    num_events += 1
                    
    if fuck_this == len(files_done):
        return None
    else:
        return files_done


#-------------------------------------------------------------------------------#
# MAIN
#-------------------------------------------------------------------------------#


if __name__ == '__main__':
    
    '''
    Not much to the old gurl, just keeps looking for new .ZIP files.
    
    basically when this is implimented the while will just become a while(1) or 
    while(true), with a 10 minute sleep timer between expected VSAT events
    There should be some sort of directory locator that then sets a
    interupt routine to break it out of sleep if a new VSAT output file
    becomes available.
    '''
    
    # List of handled .ZIP files --> should probably be kept a hold of and passed to any subsequent run events of this programme,
    # we dont want it to hand cause of trying to import a years worth of VSAT data every boot up.
    files_done = []
    
    # count is keeping track of the number of .ZIP files handled.
    # it is IMPORTANT as it is the current index for the event list,      <-- !!! this is what needs to be updated to a dictionary, and is pointed out in subsequent files
    # IE if three VSAT .ZIP files are handled, to retreive data from the 
    # third file, the index [3] MMUST be given. 
    count = 0
    
    # finds any directories containing a VSAT related .ZIP file
    all_dir = get_dir()
    
    # prompts the user for which directories to monitor
    #go_to_dir = check_dir(all_dir)
    go_to_dir = Directory_select.ask_box(all_dir)
    
    # While loop only needs to run once, running more than once will be checking 
    # for new .ZIP files to be added to the monitored directories
    # a new .ZIP must be found or the while loop will get stuck
    
    while (count < 1):
        
        for each_dir in go_to_dir:
            
            # val is the name of the .ZIP file that has been handled
            # this prevents handling a file twice REGARDLESS of if a directory
            # containes a duplicate
            
            val = get_files(each_dir, files_done, count)
            
            # if get_files indicates a .ZIP file has been handled it will return
            # None, and will move to the next 
            if ( val != None):
                files_done = val
                count += len(val)
            
            
        #time.sleep(25)
    
