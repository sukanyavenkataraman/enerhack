#
# Class for managing a schedule on one HEM

# Author: David Sehloff

import datetime
import threading
import time
from hemClient import HemClient

#startTime=datetime.datetime.now()

class hemScheduleMgr(object):
    def __init__(self, hemName, serverName, serverPort, numLoads):
        self.__hemName = hemName
        self.__serverName = serverName
        self.__serverPort = serverPort
        self.__nodes = []
        self.__numLoads = numLoads
        self.defaultLoads()
        self.initSchedule()
        self.__nodeState = {node: None for node in self.__nodes}
        self.__updateInterval=1
        self.__correctionInterval=datetime.timedelta(minutes=10)
        # Create a new HEM Client
        self.__hemClient = HemClient()
        self.__server_address = (self.__serverName, self.__serverPort)
        #self.__minOnDiff={node: None for node in self.__nodes}
        #self.__minOffDiff={node: None for node in self.__nodes}
        self.__scheduleChange = False
        self.__lastActuation = None

    def initSchedule(self):
        onTimes=[]
        offTimes=[]
        i=1
        while i <= self.__numLoads:
            onTimes.append([])
            offTimes.append([])
            i += 1
        self.__schedule = {'on':dict(zip(self.__nodes, onTimes)), 'off':dict(zip(self.__nodes, offTimes))}

    def appendOnTime(self,node, onTime):
        self.__schedule['on'][node].append(onTime)
        self.__schedule['on'][node].sort()

    def appendOffTime(self,node, offTime):
        self.__schedule['off'][node].append(offTime)
        self.__schedule['off'][node].sort()

    def extendOnTime(self,node, onTimeList):
        self.__schedule['on'][node].extend(onTimeList)
        self.__schedule['on'][node].sort()

    def extendOffTime(self,node, offTimeList):
        self.__schedule['off'][node].extend(offTimeList)
        self.__schedule['off'][node].sort()
    
    def removeOnTime(self, node, onTime):
        self.__schedule['on'][node].remove(onTime)
    
    def removeOffTime(self, node, offTime):
        self.__schedule['off'][node].remove(offTime)

    def setUpdateInterval(self, seconds):
        '''
        Set update interval of schedule executor in seconds
        '''
        self.__updateInterval=seconds
        
    def setCorrectionInterval(self, delta):
        '''
        Set correction interval of schedule executor as a timedelta
        '''
        self.__correctionInterval=delta

    def getSchedule(self):
        return self.__schedule

    def getLoads(self):
        return self.__nodes
        
    def getLoadState(self):
        return self.__nodeState

    def defaultLoads(self):
        self.__nodes = []
        i=0
        while i < self.__numLoads:
            self.__nodes.append('l'+str(i))
            i += 1

    def setLoad(self, nodeNum, newName):
        if (newName not in self.__nodes):
            try:
                self.__nodes[nodeNum]=newName
            except IndexError:
                print('setLoad could not change name of node with index '+str(nodeNum))
        else:
            print('Name given to setLoad is already in use. No change was made.')



    def setStates(self):
            self.__scheduleChange = False
            for node, onSchedule in self.__schedule['on'].items():
                dateTimeNow = datetime.datetime.now()
                minOnDiff=None
                minOffDiff=None
                for onItem in onSchedule:
                    difference = dateTimeNow-onItem
                    #Break if iteration has reached scheduled time in the future
                    if(difference.total_seconds() < 0):
                        break
                    #Save current difference if iteration is at a scheduled time that is in the past. Remove time item from list.
                    else:
                        minOnDiff=difference
                        #if (len(onSchedule)>2):
                            #self.removeOnTime(node, onItem) #remove onItem from list
                offSchedule =  self.__schedule['off'][node]
                for offItem in offSchedule:
                    difference = dateTimeNow-offItem
                    #Break if iteration has reached scheduled time in the future
                    if(difference.total_seconds() < 0):
                        break
                    #Save current difference and time item if iteration is at a scheduled time that is in the past. Remove time item from list.
                    else:
                        minOffDiff=difference
                        #if (len(offSchedule)>2):
                            #self.removeOffTime(node, offItem) #remove offItem from list
                    #Update min difference if less than previous diff and positive (scheduled time is in the future)
        
                #If no turn-on time is found in the past, set node to off
                if(minOnDiff is None):
                    if(self.__nodeState[node]!='off'):
                        self.__nodeState[node]='off'
                        self.__scheduleChange = True
                #If a turn-on time is found in the past, but no turn-off time, set node to on
                elif(minOffDiff is None):
                    if(self.__nodeState[node]!='on'):
                        self.__nodeState[node]='on'
                        self.__scheduleChange = True
                #If turn-on and turn-off times are found in the past, set node to on if turn-on time is more recent, off otherwise
                elif(minOnDiff<minOffDiff):
                    if(self.__nodeState[node]!='on'):
                        self.__nodeState[node]='on'
                        self.__scheduleChange = True
                else:
                    if(self.__nodeState[node]!='off'):
                        self.__nodeState[node]='off'
                        self.__scheduleChange = True
    
            # Return the time at which the state dict was last updated
            #updateTime = dateTimeNow

    #Data reception should always be a thread
    def receiveFromServer(self):

        #This ensures this thread is called repeatedly
        # We want to keep our ears open for any data from server
        while True:

            #Call this to get a response. 
            responseData, addressInfo = self.__hemClient.receiveResponse()


    #This is a function. Call this only when you need to send a request to server
    def sendToServer(self, apiRequest, serverAddress):

        self.__hemClient.sendRequest(apiRequest, serverAddress)

    def executeSchedule(self):
        #set states and actuate once, then start loop
        self.setStates()
        self.actuate()
        loopStart=time.time()
        while True:
            self.setStates()
            if (self.__scheduleChange):
                #if a schedule change has occurred, send the on or off signal to all nodes to match current scheduled state
                self.actuate()
            elif((datetime.datetime.now() - self.__lastActuation) >= self.__correctionInterval):
                #if the correction interval is reached, send the on or off signals to ensure all nodes match scheduled state
                self.actuate()
            time.sleep(self.__updateInterval - (time.time()-loopStart) % self.__updateInterval)
         
      
    def actuate(self):
        self.__lastActuation=datetime.datetime.now()
        #print('Actuated:' + str(self.__lastActuation))
        for node, state in self.__nodeState.iteritems():
                if (state == 'on'):
                    nodeNumber = self.__nodes.index(node)
                    self.sendToServer('/api/turnon/'+str(nodeNumber), self.__server_address)
                else:
                    nodeNumber = self.__nodes.index(node)
                    self.sendToServer('/api/turnoff/'+str(nodeNumber), self.__server_address)



    def startExecution(self):
        threads = []
        t = threading.Thread(target=self.receiveFromServer)
        threads.append(t)
        t.start()

        t = threading.Thread(target=self.executeSchedule)
        threads.append(t)
        t.start()



