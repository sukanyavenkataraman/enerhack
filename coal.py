'''
An interface that talks to the web app, talks to energyan and gets info from pvlib/cv
'''

import sys
import time
import datetime
import pv
import sendEmail

sys.path.insert(1,'../')
from module.hemSuperClient import HemSuperClient

ENERHACK_IP = "192.168.1.159"
ENERHACK_PORT = 9931

API_OFF_PRE = "/api/turnoff/"
API_ON_PRE = "/api/turnon/"

AREA = 1

import usermodes

class EnerHackCommunicator:
    def __init__(self):
        self.priorityList = [0,1,2,3,4,5,6,7]
        self.sleepTimes = [5,5,5,10,10,10,10,10]
        self.nodeToEquip = {1: 'Light1', 2: 'Light2', 3: 'Light3', 4: 'Fan1', 5: 'Misc1', 6: 'Misc2', 7: 'Misc3',
                            8: 'Misc4'}

        print ('Initialising user modes and nodes...')
        self.usage_modes = usermodes.UserModes(self.priorityList, self.sleepTimes) # Default
        self.mode = 2 # Default mode is 'meh'

        print ('Going to now connect with energyan! :D')
        # Connect and set up callbacks
        self.hemSuperClient = HemSuperClient(ENERHACK_IP, ENERHACK_PORT)
        self.hemSuperClient.subscribe(self.onReceive)
        self.power = [[0]*8]

        self.cloudcover_energy = []
        self.prevday = datetime.date.today() - datetime.timedelta(1)
        self.poll()

    def setNewMode(self, mode):
        self.mode = mode

    def setNewPriorityList(self, priorityList):
        for i in range(len(priorityList)):
            self.usage_modes.setPriority(priorityList[i], i+1)
        self.usage_modes.sortNodes()

    def setNewSleepTime(self, node, sleeptime):
        self.usage_modes.setSleepTimes(node, sleeptime)

    def setSwitchStatus(self, node, status=0, setopp=False):
        print (node, status, setopp)
        self.usage_modes.setSwitchStatus(node, status, setopp)

    def getUsageStatus(self):
        return self.power

    def getNewMode(self):
        try:
            with open('modestatus.txt', 'r') as f:
                mode = f.readlines()
                for i in range(len(mode)-1, -1, -1):
                    try:
                        newmode = int(mode[i].strip())
                        self.setNewMode(newmode)
                    except:
                        break
                    break
                f.flush()
                f.close()

            with open('modestatus.txt', 'w') as f:
                f.close()
        except:
            return

    def getToggleStatus(self):
        time.sleep(1)
        with open('nodestatus.txt', 'r') as f:
            nodes = f.readlines()
            print ('nodes to be toggled are - ', nodes)
            for n in nodes:
               try:
                   node = int(n.strip())
                   self.setSwitchStatus(node, setopp=True)
               except:
                   break
            f.flush()
        f.close()

        with open('nodestatus.txt', 'w') as f:
            pass
        f.close()

    def getPriorityStatus(self):
        try:
            with open('prioritystatus.txt', 'r') as f:
                # Assumes that priority comes in as a comma separated list
                priority = f.readlines()

                # Read only if there's only one line
                if len(priority) == 1:
                    parts = priority[0].split(',')
                    pri = []
                    for i in range(len(parts)):
                       try:
                           node = int(parts[i].strip())
                           pri.append(node)
                       except:
                           break
                f.flush()
                f.close()

            with open('prioritystatus.txt', 'w') as f:
                f.close()

            self.setNewPriorityList(pri)
        except:
            return

    def getNewSleepTime(self):
        try:
            with open('sleeptime.txt', 'r') as f:
                # Assumes that priority comes in as a comma separated list
                sleeptimes = f.readlines()

                # in the format - <node, time>
                for s in sleeptimes:
                    parts = s.strip().split(',')

                    if len(parts) == 2:
                        self.setNewSleepTime(int(parts[0]), int(parts[1]))
                f.flush()
                f.close()

            with open('sleeptime.txt', 'w') as f:
                f.close()
        except:
            return

    def writePowerUpdates(self):
        try:
            with open('powerusagestatus.txt', 'a+') as f:
                if len(self.power[-1]) == 8:
                    allnodes = self.usage_modes.nodes
                    allnodes.sort(key=lambda n: n.num)
                    toprint = ''
                    for i in range(len(self.power[-1])):
                        toprint += str(allnodes[i].status) +':' +str(self.power[-1][i]) + ','
                    f.write(toprint[:-1]+'\n')

                    with open('powerusagestatus_all.txt', 'a+') as f1:
                        f1.write(toprint[:-1]+'\n')
                        f1.flush()
                    f1.close()
                f.flush()
            f.close()
        except:
            print ('nothing to append?')
            return

    def writeSuggestions(self):
        with open('suggestions.txt', 'a+') as f:
            if len(self.cloudcover_energy) > 1:
                if self.cloudcover_energy[-1][1] < 0:
                    f.write('HIGH ALERT!!! Very low power supply for the next 3 hours' + '\n')
                    sendEmail.sendEmail('HIGH ALERT!!! Going into disaster mode... ')
                    self.mode = 4

                if self.cloudcover_energy[-1][0] - self.cloudcover_energy[-2][0] < -0.3:
                    max_usage = max(self.usage_modes[-1][:])
                    if max_usage > 20:
                        node = self.usage_modes[-1].index(max_usage)
                        f.write('Cloudy hours ahead! Maybe you could think about switching off '+ str(self.nodeToEquip[node+1]) + '\n')

                if self.cloudcover_energy[-1][1] - self.cloudcover_energy[-2][1] < -20:
                    max_usage = max(self.usage_modes[-1][:])
                    if max_usage > 10:
                        node = self.usage_modes[-1].index(max_usage)
                        f.write('Expect a drop in power supply... Maybe you could think about switching off '+ str(self.nodeToEquip[node + 1])+ '\n')
            f.flush()
            f.close()

    def writeCurrPower(self):
        try:
            with open('energystatus.txt', 'a+') as f:
                totenergy = sum(self.power[-1][:])

                f.write(str(self.cloudcover_energy[-1][0])+','+str(self.cloudcover_energy[-1][1])+','+str(totenergy))
                f.write('\n')
                f.close()
        except:
            return


    def writeTrendsFor7Days(self):

        p = []
        cc = []

        if self.prevday == datetime.date.today():
            return

        for i in range(6):
            power , cloudcover = pv.get_irradiance(time=datetime.date.today() + datetime.timedelta(i+1) + datetime.timedelta(hours=-5), intervals_of_3=8)

            for po in power[2:9]:
                p.append(po)

            for c in cloudcover[2:9]:
                cc.append(c)

        with open('next6days.txt', 'w') as f:
            towrite = ''
            for i in range(len(p)):
                towrite += str(cc[i]) + ':' + str(p[i]) + ','

            f.write(towrite[:-1]+'\n')

        f.close()

    def poll(self):
        # Default turn atleast one light on

        self.writeTrendsFor7Days()

        while (1):
            print ('Sending request')
            self.hemSuperClient.sendRequest("api/getdcpower/all")

            hour = datetime.datetime.now().hour
            month = datetime.datetime.now().month

            currPower, cloudCover  = pv.get_irradiance()
            self.cloudcover_energy.append((cloudCover[0], currPower[0]+100))
            #cloudCover = 0.5
            #currPower = 100  # Change this to get it from pvlib
            print (cloudCover, currPower)

            # Get statuses
            self.getToggleStatus()
            self.getPriorityStatus()
            self.getNewMode()

            print ('Going to configure a mode...')
            self.usage_modes.modeSelect(self.mode, cloudCover[0], currPower[0]+100, hour, month, self.power)

            # Turn off/on based on what we just did
            print ('Going to now turn on and off based on what we calculated...')

            for n in self.usage_modes.nodes:
                if n.status == 0:
                    print ('Going to turn off node ', n.num)
                    self.hemSuperClient.sendRequest(API_OFF_PRE + str(n.num))
                else:
                    print ('Going to turn on node ', n.num)
                    self.hemSuperClient.sendRequest(API_ON_PRE + str(n.num))

            self.writePowerUpdates()
            self.writeSuggestions()
            self.writeCurrPower()

            print ('Done.')
            time.sleep(3)

    def onReceive(self, message, address):
        # {u'NODE': u'ALL', u'TYPE': u'DCPOWER', u'VALUE': [0.185, 5.9, 85.6, 10.4, 0, 0, 0, 12.5]} ('192.168.1.236', 9931)

        print ('Received a message')
        print(message['VALUE'])
        totalPower = sum(message['VALUE'])
        print("Total power consumption: " + str(totalPower))

        if len(message['VALUE']) == 8:
            print (message['VALUE'])
            self.power.append(message['VALUE'])

obj = EnerHackCommunicator()
