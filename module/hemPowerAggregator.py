# 
# This is a power aggregator for nodes
# Since multiple nodes can be connected to a source/load, this module can aggregate all this data 
# based on the type. It will sum up all data of nodes connected to source or a load or something else. 

# Author: Ashray Manur

class HemPowerAggregator:

    xPow = {}
    yPow = {}

    pvValue = 0
    loadValue = 0
    chargerValue = 0
    pvCounter = 0
    chargerCounter = 0
    loadCounter = 0
    pvNodeType = ''
    loadNodeType= ''
    chargerNodeType = ''



    def __init__(self, nodes):

        self.nodes = nodes

        #nodes = {'pv': ['0', '1', '2'], 'load' = ['4','5','6','7'], 'charger': ['3']}

    def addToPowerList(self, paramData):
        #print 'adding to list'

        #value = # {'type' : VOLT, 'value' : 13.65, 'node': 0, 'date': 2017-12-08 02:28:40}

        #print paramData

        for key, val in self.nodes.iteritems():
            #print val
            if ((paramData['node'] in val) and (key=='pv')):
         
                HemPowerAggregator.pvNodeType = 'PV'
                HemPowerAggregator.pvValue = HemPowerAggregator.pvValue + float(paramData['value'])
                HemPowerAggregator.pvDate = paramData['date']
                HemPowerAggregator.pvCounter = HemPowerAggregator.pvCounter + 1

            elif(paramData['node'] in val and key=='load'):
                HemPowerAggregator.loadNodeType= 'Loads'
                HemPowerAggregator.loadValue = HemPowerAggregator.loadValue + float(paramData['value'])
                HemPowerAggregator.loadDate = paramData['date']
                HemPowerAggregator.loadCounter = HemPowerAggregator.loadCounter + 1

            elif(paramData['node'] in val and key=='charger'):
                HemPowerAggregator.chargerNodeType = 'charger'
                HemPowerAggregator.chargerValue = HemPowerAggregator.chargerValue + float(paramData['value'])
                HemPowerAggregator.chargerDate = paramData['date']
                HemPowerAggregator.chargerCounter = HemPowerAggregator.chargerCounter + 1
 

        if(HemPowerAggregator.pvCounter == len(self.nodes['pv']) and HemPowerAggregator.loadCounter == len(self.nodes['load']) and HemPowerAggregator.chargerCounter == len(self.nodes['charger'])):
        
            if (HemPowerAggregator.yPow.has_key(HemPowerAggregator.pvNodeType) and HemPowerAggregator.xPow.has_key(HemPowerAggregator.pvNodeType) and HemPowerAggregator.yPow.has_key(HemPowerAggregator.loadNodeType) and HemPowerAggregator.xPow.has_key(HemPowerAggregator.loadNodeType) and HemPowerAggregator.yPow.has_key(HemPowerAggregator.chargerNodeType) and HemPowerAggregator.xPow.has_key(HemPowerAggregator.chargerNodeType)):

                self.tempListPv = HemPowerAggregator.yPow[HemPowerAggregator.pvNodeType]
                self.tempListPv.append(HemPowerAggregator.pvValue) 
                self.tempTimeListPv = HemPowerAggregator.xPow[HemPowerAggregator.pvNodeType]
                self.tempTimeListPv.append(HemPowerAggregator.pvDate)

                self.tempListLoad = HemPowerAggregator.yPow[HemPowerAggregator.loadNodeType]
                self.tempListLoad.append(HemPowerAggregator.loadValue) 
                self.tempTimeListLoad = HemPowerAggregator.xPow[HemPowerAggregator.loadNodeType]
                self.tempTimeListLoad.append(HemPowerAggregator.loadDate)  

                self.tempListCharger = HemPowerAggregator.yPow[HemPowerAggregator.chargerNodeType]
                self.tempListCharger.append(HemPowerAggregator.chargerValue) 
                self.tempTimeListCharger = HemPowerAggregator.xPow[HemPowerAggregator.chargerNodeType]
                self.tempTimeListCharger.append(HemPowerAggregator.chargerDate)

                HemPowerAggregator.pvCounter =0
                HemPowerAggregator.loadCounter=0
                HemPowerAggregator.chargerCounter=0

                HemPowerAggregator.pvValue = 0
                HemPowerAggregator.loadValue = 0
                HemPowerAggregator.chargerValue = 0


            else:
                self.tempListPv = []
                self.tempTimeListPv = []
                self.tempListPv.append(HemPowerAggregator.pvValue)
                self.yPow[HemPowerAggregator.pvNodeType] = self.tempListPv
                self.tempTimeListPv.append(HemPowerAggregator.pvDate)
                HemPowerAggregator.xPow[HemPowerAggregator.pvNodeType] = self.tempTimeListPv

                self.tempListLoad = []
                self.tempTimeListLoad = []
                self.tempListLoad.append(HemPowerAggregator.loadValue)
                HemPowerAggregator.yPow[HemPowerAggregator.loadNodeType] = self.tempListLoad
                self.tempTimeListLoad.append(HemPowerAggregator.loadDate)
                HemPowerAggregator.xPow[HemPowerAggregator.loadNodeType] = self.tempTimeListLoad

                self.tempListCharger = []
                self.tempTimeListCharger = []
                self.tempListCharger.append(HemPowerAggregator.chargerValue)
                HemPowerAggregator.yPow[HemPowerAggregator.chargerNodeType] = self.tempListCharger
                self.tempTimeListCharger.append(HemPowerAggregator.chargerDate)
                HemPowerAggregator.xPow[HemPowerAggregator.chargerNodeType] = self.tempTimeListCharger

                HemPowerAggregator.pvCounter =0
                HemPowerAggregator.loadCounter=0
                HemPowerAggregator.chargerCounter=0

                HemPowerAggregator.pvValue = 0
                HemPowerAggregator.chargerValue = 0
                HemPowerAggregator.loadValue = 0


    def returnPowerObject(self):

        return HemPowerAggregator.yPow, HemPowerAggregator.xPow











