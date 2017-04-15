

'''
Luke Reisima
Version 1

Current version date:
15/04/2017

File contains:
1. Finding the Zip directory (anywhere),
2. Un-zipping into a tmp file
3. reading data out of the .tmp file into the .lmt structure
4. deleting the .tmp file

- Parent --> none
- Child --> read_LMT_data_in

Reliant on:
- See Importing section

Code Explanation:
- Fully do string'd and commented
Otherwise ask Luke - 0278645084

Date Fully functional:
--- not yet ---

Work to complete:
- Directory search is too broad, it'll pick up ALL VSAT .ZIP files
   --> this needs to be refined to only pick up new/relevant VSAT files
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


#-------------------------------------------------------------------------------#
# Globals
#-------------------------------------------------------------------------------#


# Event is the broadest data structure, it contains one run time worth of VSAT points
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
                        

def get_files(files_done, num_events):
    
    '''
    get_files does the search for any VSAT related .ZIP files
    
    !!! -->
    Currently the search is too broad and covers the entire mac directory
    Because of this it needs to ommit the google drive synch folder I have
    <-- !!!
    
    It passes the file directory path back to main if A NEW .ZIP file is found
    '''
    
    # /Users is the highest level in the mac OS
    # os.walk() allows iteration though the file system
    for root, _, files in os.walk("/Users"):
        for f in files:
            fullpath = os.path.join(root, f)
            
            # checking if the file name holds a VSAT related suffix
            # and ignoring unrelated directories by SPECIFIC exemption
            if ("NDT_P0.ZIP" in fullpath) and not("Google" in fullpath):
                
                # Checking for if the .ZIP file has already been targeted
                if fullpath not in files_done:
                    
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
                    return fullpath


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
    
    # will need to increase for the number of VSAT events stored, ie i'm only testing with two
    while (count < 2):
        
        val = get_files(files_done, count)
        if ( val != None):
            files_done.append(val)
        count += 1
            
        #time.sleep(25)
    
