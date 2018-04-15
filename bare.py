import sys
import time

sys.path.insert(1,'../')
from module.hemSuperClient import HemSuperClient

ENERHACK_IP = "192.168.1.159"
ENERHACK_PORT = 9931

class EnerHackCommunicator:
	def __init__(self, priorityList, maxAllowedPowerConsumption):
		self.maxAllowedPowerConsumption = maxAllowedPowerConsumption
		self.priorityList = priorityList
		
		# Connect and set up callbacks
		self.hemSuperClient = HemSuperClient(ENERHACK_IP, ENERHACK_PORT)
		self.hemSuperClient.subscribe(self.onReceive)
		
		self.poll()
	
	def poll(self):
		self.hemSuperClient.sendRequest("/api/turnon/1")
		#self.hemSuperClient.sendRequest("/api/turnon/2")
		#self.hemSuperClient.sendRequest("/api/turnon/3")
		#self.hemSuperClient.sendRequest("/api/turnon/7")
		while(1):
			self.hemSuperClient.sendRequest("api/getdcpower/all")
			time.sleep(3)

	def onReceive(self, message, address):
		#{u'NODE': u'ALL', u'TYPE': u'DCPOWER', u'VALUE': [0.185, 5.9, 85.6, 10.4, 0, 0, 0, 12.5]} ('192.168.1.236', 9931)
		print(message['VALUE'])
		totalPower = sum(message['VALUE'])
		print("Total power consumption: " + str(totalPower))
		if totalPower > self.maxAllowedPowerConsumption:
			#TO-DO: Turn off according to priority list
			self.hemSuperClient.sendRequest("/api/turnoff/2")
			self.hemSuperClient.sendRequest("/api/turnoff/3")
			print("Turned off nodes")

obj = EnerHackCommunicator([], 70)			

