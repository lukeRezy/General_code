



zones = ['GOSZONE9', 'GZ14_TWI', 'GOSZONE5', 'ZONE3', 'ZONE1', 'GOSZONE1', 'GZ12_HOR', 'GZ678']
trends = {}
for zone in zones:
    trends[zone] = {}
    for X in range (0, 2):
        trends[zone][source1] = []
        trends[zone][source2] = []
        if X//2 == 0:
            trends[zone][source1].append(Event.VSAT_event[VSAT_num].transfer[zone].data_select['TransferSources'].data_cont['Source1'].data_val['Initial'])
        else:
            trends[zone][source2].append(Event.VSAT_event[VSAT_num].transfer[zone].data_select['TransferSources'].data_cont['Source2'].data_val['Initial'])
