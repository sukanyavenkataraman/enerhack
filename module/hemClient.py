# 
# This module is used to pull data from HEMApp 

# Author: Ashray Manur

import sys 
import socket
import json

class HemClient:

	def __init__(self):

		#Create a new UDP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



	def sendRequest(self, apiCall, server_address):

		#Send a request to UDP server in HEMApp with API Call
		self.sock.sendto(apiCall, server_address)




	def receiveResponse(self):

		#Receieve response from UDP server
		self.data, self.addr = self.sock.recvfrom(1024)
		
		#print self.addr
		self.data = self.data.rsplit("}" , 1)[0]
		self.data = "".join([self.data, "}"])

		try:
			self.parsedData = json.loads(self.data)
		except ValueError as e:
			errorResponse= {}
			errorResponse['NODE'] = 'ALL'
			errorResponse['TYPE'] = 'ERROR'
			errorResponse['VALUE'] = 'INVALID REQUEST'
			self.parsedData = json.dumps(errorResponse)
			return self.parsedData, self.addr
		#Returns a dict with a key value pair and a tuple
		return self.parsedData, self.addr

