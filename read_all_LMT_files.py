

'''
Luke Reisima
Version 1

Current version date:
14/04/2017

File contains:
Opening the .LMT data files.
- Parent --> none
- Child --> read_LMT_data_in

Reliant on:
- xml.etree.ElementTree as imported in the parent

Code Explanation:
- doc string'd and commented.
- this is real basic dw about it.
Otherwise ask Luke - 0278645084

Date Fully functional:
--- not yet ---
- this will be combined with Atuls unzipping and file handling programe
- unlikely to be actually used, just for testing

Work to complete:
- Replace with Atuls file handler

'''

# XML data handling
import read_LMT_data_in as store_LMT

# XML file handling library
import xml.etree.ElementTree as ET

# .LMT data structure
import LMT_data_struct

if __name__ == '__main__':
    
    ''' 
    This is real basic, it just changes the last number of 
    the .lmt file to import all .lmt files in one VSAT 
    run event, this is all assuming there are only 8 .LMT files.
    There really isn't much more to this file
    '''
    
    
    base = "vt2017_03_10_00_01_06_ndt_p0_"
    extn = "-lmt.xml"
    num = 201
    Event = LMT_data_struct.VSAT_out()
    Event.add_event()
    
    while num < 1010:
        
        # this is where we are assuming there are only 8 .LMT files
        
        tree = ET.parse(base + str(num) + extn)
        root = tree.getroot()
        store_LMT.read_into_struct(root,0,Event)
        num += 101
        
    #print("\n \n this is the start of test outputs \n ####################### \n \n")
    #print(store_LMT.fetch_data(Event, 0, "ZONE3", "TransferSources", "Source2", "Initial"))    

