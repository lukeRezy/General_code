
        
class data_type (object):
    
    def __init__(self):
        
        '''
        Data_type is the nested dictionary from a zone, it splits the contingency
        data into related fields   
        '''
        
        self.data_select = {}
        
    
    def add_data (self, data_location, data_ID, data_val):
        
        ''' 
        Add_data creates a further nested dictionary
        the data_location is the umbrella'd related data
        data_ID is the specific data point with correspinding value: data_val
        '''
        
        self.data_select[data_location] = {}
        self.data_select[data_location][data_ID] = data_val       
        
        
class Zone (object):
    
    def __init__(self):
        
        '''
        Zone is a dictionary contining the specific 14 zones transpower monitors,
        OR contains the zones specific to the VSAT run event
        '''
        
        self.zone = {}
    
    
    def add_zone (self, zone_name):
        
        '''
        Adding a zone creates the key value pair of "zone ID" to "zone Contingency data"
        calles data_type, as above -->
        '''
        
        self.zone[zone_name] = data_type()
        

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
        (LMT) file becomes available. It also calles Zone() - see above -->
        '''
        
        self.VSAT_event.append(Zone())


if __name__ == '__main__':
    # create a VSAT data output handling structure
    Event1 = VSAT_out() 
    
    # to add an event:
    Event1.add_event()
    
    # add a zone contingency:
    Event1.VSAT_event[0].add_zone('GZ8')
    
    # create a data class within a zone contingency:
    Event1.VSAT_event[0].zone['GZ8'].add_data("basic_data", "trans_name", "ben-twi")
    Event1.VSAT_event[0].zone['GZ8'].add_data("monitored_voltages", "bus", "ben")
    Event1.VSAT_event[0].zone['GZ8'].add_data("monitored_flow", "initial_flow", 181)
    
    # how to call a specific data point
    print (Event1.VSAT_event[0].zone['GZ8'].data_select["basic_data"]["trans_name"])
    
    # or for example
    aaa = (Event1.VSAT_event[0].zone['GZ8'].data_select["basic_data"]["trans_name"])
    bbb = (Event1.VSAT_event[0].zone['GZ8'].data_select["monitored_voltages"]["bus"])
    ccc = (Event1.VSAT_event[0].zone['GZ8'].data_select["monitored_flow"]["initial_flow"])
    
    print ('transfer name: "{}", Voltage monitored at bus: "{}", with flow of: "{}MW"'.format(aaa, bbb, ccc))
    # to add another event:
    # Event1.add_event()
    # Event1.VSAT_event[1].add_zone('GZ8')
    
    ''' 
    Data structure overview:
    
    - Event is the broadest OBJECT, it contains everything else:
    - VSAT_event is the LIST of VSAT outputs
    - zone is a DICTIONARY where the zone name is the KEY, and the VALUE is a nested dictionary containing contingencies
    - Data select contians TWO NESTED DICTIONARIES
        --> the first KEY is the contingency with a VAUE as the nested dictionary containing data points
        --> the second KEY is the data point identifier and the VALUE is the final data point
    '''