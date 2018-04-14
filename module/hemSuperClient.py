# 
# This is the new HEMClient. It provides better abstraction through publish/subscribe
# Author: Ashray Manur

import sys 
import socket
import json
import threading
import uuid 

class HemSuperClient:


	def __init__(self, serverIp, serverPort):

		#Create a new UDP socket
		self.serverIp = serverIp
		self.serverPort = serverPort
		self.serverAddress = (self.serverIp, self.serverPort)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.parsedData = ''
		self.publisher = HemPublisher()
		self.threads = []
		t = threading.Thread(target=self.receiveResponse)
		self.threads.append(t)
		t.start()


	def sendRequest(self, apiCall):

		#Send a request to UDP server in HEMApp with API Call
		self.sock.sendto(apiCall.encode('utf8'), self.serverAddress)


	def receiveResponse(self):
		while True:
			#Receieve response from UDP server
			self.data, self.addr = self.sock.recvfrom(1000)
			self.data = self.data.decode('utf8')
			
			#print self.addr
			self.data = self.data.rsplit("}" , 1)[0]
			self.data = "".join([self.data, "}"])

			try:
				self.parsedData = json.loads(self.data)
				#print self.parsedData
			except ValueError as e:
				errorResponse= {}
				errorResponse['NODE'] = 'ALL'
				errorResponse['TYPE'] = 'ERROR'
				errorResponse['VALUE'] = 'INVALID REQUEST'
				self.parsedData = json.dumps(errorResponse)
				#return self.parsedData, self.addr
			#Returns a dict with a key value pair and a tuple
			#return self.parsedData, self.addr
			self.publisher.dispatch(self.parsedData, self.addr)

	def subscribe(self, callback):
		functionId = str(uuid.uuid4())
		self.publisher.register(functionId, callback)

class HemPublisher:

	def __init__(self):
		self.subscribers = dict()
	def register(self, who, callback=None):
		if callback is None:
			callback = getattr(who, 'update')
			print(callback)
		self.subscribers[who] = callback

	def unregister(self,who):
		del self.subscribers[who]

	def dispatch(self,message, address):
		for subscriber, callback in self.subscribers.items():
			callback(message, address)