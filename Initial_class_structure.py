
class initial_data:
    """ class for aggregating data defined to one contingency """
    
    def __init__(self, trans_name, initial_NIGENS, max_NIGENS, min_NIGENS, initial_transfer, max_transfer, min_transfer):
        self.trans_name = trans_name
        self.init_NIGENS = initial_NIGENS
        self.max_NIGENS = max_NIGENS
        self.min_NIGENS = min_NIGENS
        self.initial_transfer = initial_transfer
        self.max_transfer = max_transfer
        self.min_transfer = min_transfer
        
        
class contingency_limit (object):
    
    def __init__(self,lim_point_num,lim_NIGENS,lim_gen,violation_point, violation_NIGENS, violation_gen, violation_contingency):
        self.lim_point = lim_point_num
        self.lim_NIGENS = lim_NIGENS
        self.lim_zone_gen = lim_gen
        self.lim_cont = lim_cont
        self.vio_point = violation_point
        self.vio_NIGENS = violation_NIGENS
        self.vio_gen = violation_gen
        self.vio_cont = violation_contingency
        
class monitored_voltages (object):
     
    def __init__(self,bus, design_volt, ID, init_v, pre_v, ins_v, post_v, stab_v, max_min_v):
        self.bus = bus
        self.bus_volt = design_volt
        self.bus_ID = ID
        self.initial_voltage = init_v
        self.pre_voltage = pre_v
        self.insecure_voltage = ins_v
        self.post_voltage = post_v
        self.stability_limit = stab_v
        self.max_min = max_min

class monitored_flow (object):
    
    def __init__(self, interface_name, flow_type, initial_flow, pre_flow, insecure_flow, post_flow, stability_flow, max_min_flow):
        self.interface_name = interface_name
        self.flow_type = flow_type
        self.initial_voltage = initial_flow
        self.pre_flow = pre_flow
        self.insecure_flow = ins_flow
        self.post_flow = post_flow
        self.stability_limit = stab_flow
        self.max_min = max_min_flow
        
class contingency (object):
    
    def __init__(self,interface_name, flow_type, initial_flow, pre_flow, insecure_flow, post_flow, stability_flow, max_min_flow, bus, design_volt, ID, init_v, pre_v, ins_v, post_v, stab_v, max_min_v, lim_point_num,lim_NIGENS,lim_gen,violation_point, violation_NIGENS, violation_gen, violation_contingency, trans_name, initial_NIGENS, max_NIGENS, min_NIGENS, initial_transfer, max_transfer, min_transfer):
        self.flow = monitored_flow(interface_name, flow_type, initial_flow, pre_flow, insecure_flow, post_flow, stability_flow, max_min_flow)
        self.voltage = monitored_voltage(bus, design_volt, ID, init_v, pre_v, ins_v, post_v, stab_v, max_min_v)
        self.contingency = contingency_limit(lim_point_num,lim_NIGENS,lim_gen,violation_point, violation_NIGENS, violation_gen, violation_contingency)
        self.about = initial_data(trans_name, initial_NIGENS, max_NIGENS, min_NIGENS, initial_transfer, max_transfer, min_transfer)
        