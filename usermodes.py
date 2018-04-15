'''
4 different modes -
1. Super saver (automatic, app have full control)
2. Meh (I don't really care)
3. I'm a coal miner (I will use as much as I want)
4. 2012 (Disaster is coming)

Different configurations for each mode

Node 1 - Light1
Node 2 - Light2
Node 3 - Light3
Node 4 - Fan1
Node 5-8 - Misc
'''

class Nodes(object):
    def __init__(self, node, priority, sleepTime):
        self.num = node
        self.sleepTime = sleepTime
        self.priority = priority
        self.status = 0

class UserModes(object):
    def __init__(self, priorityList, sleepTime):
        self.modes = {1:'Super Saver', 2:'Meh', 3:'I\'m a coal miner', 4:'2012'}
        self.priorityList = priorityList
        self.month_time = {1:17, 2:17, 3:17, 4:18, 5:18, 6:18, 7:19, 8:19, 9:19, 10:18, 11:17, 12:17}

        self.nodes = []
        for i in range(len(self.priorityList)):
            self.nodes.append(Nodes(self.priorityList[i], i, sleepTime[self.priorityList[i]]))

        self.sortNodes()

    def sortNodes(self):
        self.nodes.sort(key=lambda n: n.priority)

    def setPriority(self, node, priority):
        for n in self.nodes:
            if n.num == node:
                n.priority = priority
                break

    def setSleepTimes(self, node, sleeptime):
        for n in self.nodes:
            if n.num == node:
                n.sleepTime = sleeptime
                break

    def printModes(self):
        print (self.modes)

    def setSwitchStatus(self, node, status, setopp=False):
        for n in self.nodes:
            if n.num == node:
                n.status = status if not setopp else int(not n.status)

    def modeSelect(self, mode, cloudcover, availenergy, hour, month, usage):

        if mode == 1:
            print ('You have selected - ', self.modes[mode], ' mode')
            self.superSaverMode(cloudcover, availenergy, hour, month, usage)

        elif mode == 2:
            print ('You have selected - ', self.modes[mode], ' mode')
            self.mehMode(availenergy, usage)

        elif mode == 3:
            print ('You have selected - ', self.modes[mode], ' mode')
            self.donaldTrumpMode()

        elif mode == 4:
            print ('You have selected - ', self.modes[mode], ' mode')
            self.disasterMode(availenergy, usage)

        else:
            print ('You have selected an invalid mode. Going into default ', self.modes[2], ' mode')
            self.mehMode(availenergy)

    def reducePower(self, availPower, currPower, usage):
        # If energy greater than, then turn off multiple

        while currPower >= availPower:
            for i in range(len(self.nodes)):
                currPower -= usage[-1][self.nodes[i].num]
                self.nodes[i].status = 0

        return currPower

    def controlSleep(self, usage):

        for i in range(len(self.nodes)):
            # Because we poll every 3s
            if len(usage) > self.nodes[i].sleepTime:
                if usage[-1][self.nodes[i].num] - usage[-1-self.nodes[i].sleepTime][self.nodes[i].num] - 3 < 0.01:
                   self.nodes[i].status = 0

    def superSaverMode(self, cloudcover, availPower, hour, month, usage):

        currPower = sum(usage[-1][:])

        print ('currPower is - ', currPower)

        # Reduce energy first
        if currPower >= availPower:
            currPower = self.reducePower(availPower, currPower, usage)

        # Put things to sleep
        self.controlSleep(usage)

        # Turn on/Turn off
        if cloudcover < 0.3 and 6 <= hour < self.month_time[month]:
            for n in self.nodes:
                if n.num in (0, 1, 2) and n.priority <= 2:
                    n.status = 0
                    currPower -= usage[-1][n.num]

        elif cloudcover < 0.5:
            for n in self.nodes:
                if n.num in (1,2,3) and n.priority == 0:
                    n.status = 0
                    currPower -= usage[-1][n.num]
                    break

        elif hour < 22: # Don't randomly switch on lights after 10 o clock!
            for i in range(len(self.nodes)):
                if self.nodes[i].num in (0,1,2):
                    if currPower + usage[-1][self.nodes[i].num] < availPower:
                        self.nodes[i].status = 1
                        currPower += usage[-1][self.nodes[i].num]

        print ('curr power is now - ', currPower)

    def mehMode(self, availPower, usage):

        currPower = sum(usage[-1][:])

        print ('currPower is - ', currPower, ' available power is - ', availPower)
        # Only energy to get under the max available
        if currPower >= availPower:
            print ('Energy usage is going over the limit, turning off some lights')
            currPower = self.reducePower(availPower, currPower, usage)

        print ('currPower will now be - ', currPower)

    def donaldTrumpMode(self):
        print ('Not doing anything because there exists unlimited electricity in this world...')

    def disasterMode(self, availPower, usage):
        print ('Going to keep only one light and misc node 5 allowed to be kept on')

        # Get light with topmost priority
        lightnode = 0

        for i in range(len(self.nodes)-1,-1,-1):
            if self.nodes[i] in (0,1,2):
                lightnode = self.nodes[i].num
                break

        miscnode = 4

        # First make sure power consumption is lesser than allowed value
        currPower = sum(usage[-1][:])

        if currPower >= availPower:
            print ('Energy usage is going over the limit, turning off things off')
            currPower = self.reducePower(availPower, currPower, usage)

        # Next turn off all other nodes
        for n in self.nodes:
            if n.num not in (lightnode, miscnode):
                n.status = 0






















