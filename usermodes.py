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

    def setSleepTime(self, node, sleepTime):
        self.nodeToSleepTime[node] = sleepTime

class UserModes(object):
    def __init__(self, priorityList, sleepTime):
        self.modes = {1:'Super Saver', 2:'Meh', 3:'I\'m a coal miner', 4:'2012'}
        self.priorityList = priorityList
        self.month_time = {1:17, 2:17, 3:17, 4:18, 5:18, 6:18, 7:19, 8:19, 9:19, 10:18, 11:17, 12:17}

        self.nodes = []
        for i in range(len(self.priorityList)):
            self.nodes.append(Nodes(self.priorityList[i], i, sleepTime[self.priorityList[i]]))

        self.nodes.sort(key= lambda n:n.priority)

    def setPriority(self, node, priority):
        self.nodes[node].priority = priority

    def setSleepTimes(self, node, sleeptime):
        self.nodes[node].sleepTime = sleeptime

    def printModes(self):
        print (self.modes)

    def setSwitchStatus(self, node, status):
        self.nodes[node].status = status

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
            self.disasterMode()

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
            if usage[self.nodes[i].num][-1] - usage[self.nodes[i].num][-1-self.nodes[i].sleepTime] - 3 < 0.01:
               self.nodes[i].status = 0

    def superSaverMode(self, cloudcover, availPower, hour, month, usage):

        currPower = sum(usage[-1, :])

        print ('currPower is - ', currPower)

        # Reduce energy first
        if currPower >= availPower:
            currPower = self.reducePower(availPower, currPower, usage)

        # Put things to sleep
        self.controlSleep(usage)

        # Turn on/Turn off
        if cloudcover < 0.3 and 6 <= hour < self.month_time[month]:
            for n in self.nodes:
                if n.num in (1, 2, 3) and n.priority <= 3:
                    n.status = 0
                    currPower -= usage[-1][n.num]

        elif cloudcover < 0.5:
            for n in self.nodes:
                if n.num in (1,2,3) and n.priority == 1:
                    n.status = 0
                    currPower -= usage[-1][n.num]
                    break

        else:
            while currPower < availPower:
                for i in range(len(self.nodes)):
                    if self.nodes[i].num in (1,2,3):
                        self.nodes[i].status = 1
                        currPower += usage[-1][self.nodes[i].num]

        print ('curr power is now - ', currPower)

    def mehMode(self, availPower, usage):

        currPower = sum(usage[-1][:])

        print ('currPower is - ', currPower)
        # Only energy to get under the max available
        if currPower >= availPower:
            print ('Energy usage is going over the limit, turning off some lights')
            currPower = self.reducePower(availPower, currPower, usage)

        print ('currPower will now be - ', currPower)

    def donaldTrumpMode(self):
        print ('Not doing anything because there exists unlimited electricity in this world...')

    # TODO: Fill up cases for this
    def disasterMode(self):
        print ('Going to keep only one light and misc node 5 on')
















