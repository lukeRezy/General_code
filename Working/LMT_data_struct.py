

'''
Luke Reisima
Version 2

Current version date:
14/04/2017

File contains:
Data structure for the LMT data files.
- Parent --> read_LMT_data_in
- Child --> none

Reliant on:
- none

Code Explanation:
Doc strings attached to all functions, and expanation of heirachy at the bottom
Otherwise ask Luke - 0278645084

Date Fully functional:
--- not yet ---

Work to complete:
Structure relys on a list at the highest level, needs to be updated
to use a dictionary with the date as the key, or otherwise:
- could use a dictionary at a higher level to hold index/date pairs but that
- seems like double handling data.

'''


class add_data_val (object):
    
    def __init__(self):
        '''
        add_data_val populates the lowest dictionary
        There are no lower data structures
        '''
        
        self.data_val = {}
        
    def add_data (self, data_ID, data_in):
        '''
        Add data is the lowest level and contains the 'numerical' data
        This is once more a dictionary where:
        data_ID is the specific data point with correspinding value: data_in
        '''
            
        self.data_val[data_ID] = data_in
        
class data_container (object):
    
    def __init__(self):
        
        '''
        Data container is the grouping of data within a type, for example:
        A Type: TransferSource contains two groups of data Source1 and Source2
        '''
        
        self.data_cont = {}
        
    def add_data_cont (self, cont_name):
        
        '''
        Add data_container creates a grouping of busses or transfer zones
        Calls add_data avove -->
        '''
        
        self.data_cont[cont_name] = add_data_val()
        
class data_type (object):
    
    def __init__(self):
        
        '''
        Data_type is the nested dictionary from a transfer, it splits the contingency
        data into related fields   
        '''
        
        self.data_select = {}
        
    
    def add_data_type (self, data_location):
        
        ''' 
        Add_data_type creates a further nested dictionary
        the data_location is the umbrella'd related data
        calls data_container as above -->
        '''
        
        self.data_select[data_location] = data_container() 
        
        
class transfer (object):
    
    def __init__(self):
        
        '''
        transfer is a dictionary contining the specific 14 transfers transpower monitors,
        OR contains the transfers specific to the VSAT run event
        '''
        
        self.transfer = {}
    
    
    def add_transfer (self, transfer_name):
        
        '''
        Adding a transfer creates the key value pair of "transfer ID" to "transfer Contingency data"
        calles data_type, as above -->
        '''
        
        self.transfer[transfer_name] = data_type()
        

class VSAT_out (object):
    '''
    eventually make this a linked list not just a list, for the logical flow
    of the vsat events. (linked list as a circbuff maybe?)
    '''
    
    def __init__(self):
        
        '''
        init creates the list of events which is the highest level data structure
        '''
        
        self.VSAT_event = []
        
        
    def add_event(self):
        
        '''
        Add_events appends to the list every 15 minutes, or as a new VSAT output 
        (LMT) file becomes available. It also calles transfer() - see above -->
        '''
        
        self.VSAT_event.append(transfer())
        
        ########################################################################

### NOTE ###
### from here down is ONLY explanatory, it is not part of the data structure ###

'''
        
if __name__ == '__main__':
    # create a VSAT data output handling structure
    Event1 = VSAT_out() 
    
    # to add an event:
    Event1.add_event()
    
    # add a transfer contingency:
    Event1.VSAT_event[0].add_transfer('GZ8')
    
    #
    Event1.VSAT_event[0].transfer['GZ8'].add_data_type('basic_data')
    Event1.VSAT_event[0].transfer['GZ8'].add_data_type('monitored_voltages')
    Event1.VSAT_event[0].transfer['GZ8'].add_data_type('monitored_flow')
    
    Event1.VSAT_event[0].transfer['GZ8'].data_select['basic_data'].add_data_cont('source1')
    Event1.VSAT_event[0].transfer['GZ8'].data_select['monitored_voltages'].add_data_cont('source1')
    Event1.VSAT_event[0].transfer['GZ8'].data_select['monitored_flow'].add_data_cont('source1')    
    
    # create a data class within a transfer contingency:
    Event1.VSAT_event[0].transfer['GZ8'].data_select['basic_data'].data_cont['source1'].add_data("trans_name", "ben-twi")
    Event1.VSAT_event[0].transfer['GZ8'].data_select["monitored_voltages"].data_cont['source1'].add_data("bus", "ben")
    Event1.VSAT_event[0].transfer['GZ8'].data_select["monitored_flow"].data_cont['source1'].add_data("initial_flow", 181)
    
    # how to call a specific data point
    print (Event1.VSAT_event[0].transfer['GZ8'].data_select["basic_data"].data_cont['source1'].data_val["trans_name"])
    
    # or for example
    aaa = (Event1.VSAT_event[0].transfer['GZ8'].data_select["basic_data"].data_cont['source1'].data_val["trans_name"])
    bbb = (Event1.VSAT_event[0].transfer['GZ8'].data_select["monitored_voltages"].data_cont['source1'].data_val["bus"])
    ccc = (Event1.VSAT_event[0].transfer['GZ8'].data_select["monitored_flow"].data_cont['source1'].data_val["initial_flow"])
    
    print ('transfer name: "{}", Voltage monitored at bus: "{}", with flow of: "{}MW"'.format(aaa, bbb, ccc))
    # to add another event:
    # Event1.add_event()
    # Event1.VSAT_event[1].add_transfer('GZ8')
    
    ''' 


### DATA STRUCTURE OVERVIEW BELOW:


'''

    Data structure overview:
    
    - Event is the broadest OBJECT, it contains everything else:
    - VSAT_event is the LIST of VSAT outputs,
        --> Ie if DSA tools is run twice, then there will be two entries of VSAT data as index 0 and index 1 respectively.
    - transfer is a DICTIONARY where the transfer name is the KEY, and the VALUE is a nested dictionary containing contingencies
        --> Ie The transfer is the individual .LMT files within a VSAT run event.
    - data_select contains groupings of data within a transfer
        --> Ie a transfer contains 3 groupings, "TransferSources", "TransferPoints", "MonitoredQuantities"
    - data_cont refers to the data container, these are further related fields of data within a grouping
        --> Ie within "transferSources" there are both "Source1" and "Source2"
    - data_val is the lowest level and contains the mumerical data
        --> Ie within "Source1" the Key "Max" within data_val will return the corresponding data point.
        
        Therefore:
    VSAT_event --> transfer --> data_select --> data_cont --> data_val = ###

'''