

'''
Luke Reisima
Version 2

Current version date:
14/04/2017

File contains:
Handling the LMT data.
- Parent --> read_all_LMT_files
- Child --> LMT_data_struct

Reliant on:
- xml.etree.ElementTree as imported in the parent

Code Explanation:
- Fully doc string'd and commended for more explanation
Otherwise ask Luke - 0278645084

Date Fully functional:
--- not yet ---

Work to complete:
- refer to LMT_data_struct
- an idea for this is commended below under the read_into_struct function

'''

def add_data(Event, event_num, transfer, data_location, data_container, data_ID, data_val):
    '''
    
    short cut into adding data into the VSAT LMT object)
    '''
    
    Event.VSAT_event[event_num].transfer[transfer].data_select[data_location].data_cont[data_container].add_data(data_ID, data_val)
    return;

def fetch_data(Event, event_num, transfer, data_location, data_container, data_ID):
    
    '''
    short cut into reading data from the VSAT LMT object)
    '''    
    
    return Event.VSAT_event[event_num].transfer[transfer].data_select[data_location].data_cont[data_container].data_val[data_ID];

def read_into_struct(root, event_num, Event):
    
    '''
    Utilises the .XML file format to read data in using the ElementTree .XML API.
    further explanation below.
    '''
    
    # Root is the overarching file and contains version data and date/time data
    
    # Reccomendation:
    # Replace the numerical list and indexed form of VSAT_event -
    # for a dictionary with the key as follows:
    # VSAT_event = Root.get("date") + "_" + Root.get("time")    
    
    for child in root:
        
        # Child is the transfer location, for example GOSZONE5
        # Forevery VSAT run event there will be a number of transfer locations.
        
        Event.VSAT_event[event_num].add_transfer(child.get("name"))
        
        # Creates a transfer data set within a VSAT run event
    
        for data_type in child:
            
            # data_type contains the larger data sets within the .LMT file:
            # 1. TransferSources
            # 2. TransferPoints
            # 3. MonitoredQuantities            
            
            Event.VSAT_event[event_num].transfer[child.get("name")].add_data_type(data_type.tag)
            
            # the lower level data structures are dependent on the broader structure
            # the IF statements sort this data into related fields
            
            if data_type.tag == "TransferSources":
                
                for data_name in data_type:
                    
                    # Data name is the lowest level of data grouping, 
                    # Contains the set of related data points
                    
                    Event.VSAT_event[event_num].transfer[child.get("name")].data_select[data_type.tag].add_data_cont(data_name.tag)
                    for data_item in data_name:
                        
                        # Data_item holds the actual data points
                        # It is a dictionary where the key is the data point identidier,
                        # and the value is the actual data point.
                        
                        add_data(Event, event_num, child.get("name"), data_type.tag, data_name.tag, data_item.tag, data_item.text.strip())

            
            if data_type.tag == "TransferPoints":
                
                # the two FOR LOOPS are due to "TransferPoints" containing two data sets.
                # see below for more
                
                for data_name in data_type:
                    
                    # same as above
                    
                    Event.VSAT_event[event_num].transfer[child.get("name")].data_select[data_type.tag].add_data_cont(data_name.tag + data_name.get("no"))
                    for kk in data_name.attrib:
                        
                        # Loop one takes the data from the first line of a transfer point,
                        # the iteration of "kk" is iterating across the keys in the final data dictionary.
                        # Ie it takes the numerical data
                        
                        add_data(Event, event_num, child.get("name"), data_type.tag, (data_name.tag + data_name.get("no")), kk, data_name.attrib[kk])
                    
                    for data_item in data_name:
                        
                        # steps over one set of "final data" and into the second line of a transfer point
                        # This is because there are two ends to the data_name branch
                        # Ie it takes the contingency name as key and violaiton type as value
                        
                        for kk in data_item.attrib:
                            
                            #Loop two 
                            
                            add_data(Event, event_num, child.get("name"), data_type.tag, (data_name.tag + data_name.get("no")), kk, data_item.attrib[kk])
            
            
            if data_type.tag == "MonitoredQuantities":
                
                # the below is creating the special data containes, explained further below also
                
                Event.VSAT_event[event_num].transfer[child.get("name")].data_select[data_type.tag].add_data_cont("kV")
                Event.VSAT_event[event_num].transfer[child.get("name")].data_select[data_type.tag].add_data_cont("MW")    
                
                # Because of the data structure there can only be one data container
                # "MonitoredQuantities" is arranged such that two contianers would be preferable
                # but that wont work for the set of monitored quantities
                # therefore the two IF conditions seperate the data into voltage and Power monitored points
                # these are then the contianers
                
                for data_name in data_type:
                    
                    # as above
                    
                    for data_item in data_name:
                        
                        # as above
                        
                        if "kV" in data_name.attrib.values():
                            for data_cont in data_item:
                                
                                # this is where the "TransferPoints" would benefit from a secondary container
                                # instead we iterate through the "values" that are contained within any given monitored point.
                                # To create the unique key's for data retreval a combination of the name, voltage and value number is used
                                # Note that value number (ie value1 or value2) convention is as follows:
                                
                                # Value1 = Initial point
                                # Value2 = Pre Contingency Limit Point
                                # Value3 = Insecure point
                                # Value4 = Post Contingency Limit point                            
                                
                                data_ID = data_item.attrib["eqname"].split()[0] + "_" + data_item.attrib["eqname"].split()[1] + "_" + data_cont.tag\
                                    
                                # as an example, data_ID:TUI_110_Value1
                                # where:
                                # bus = TUI, Nominal voltage = 110kV, pointing to the "initial point"
                                
                                add_data(Event, event_num, child.get("name"), data_type.tag, "kV", data_ID, data_cont.text)

                        if "MW" in data_name.attrib.values():
                            for data_cont in data_item:
                                
                                # as above
                                
                                data_ID = data_item.attrib["name"].split()[0] + "_" + data_cont.tag
                                add_data(Event, event_num, child.get("name"), data_type.tag, "MW", data_ID, data_cont.text)
                        

