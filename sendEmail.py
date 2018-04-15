#
# 
# Sample app to send email

# Author: Ashray Manur

import datetime
import threading
import time
import sys
import email
import email.utils
import sys

sys.path.insert(1,'../')

from module.hemSuperClient import HemSuperClient
import module.hemEmail

'''
hemSuperClient = HemSuperClient("192.168.1.159", 9931)

def update(message, address):
	print 'Rec:', message, address
	sendEmail(message['VALUE'])

#Subscribe to data from HEMs
# The argument to this is the name of the function you want triggered when you get data
hemSuperClient.subscribe(update)

'''

def sendEmail(data):

	#Before you call this, make sure you have a file with the login details in the same directory as your app
	#In this case we are using 'loginDetails.log'
	#The file should have two lines
	
	#email:myemail@email.com
	#password: mypassword

	#This is the email and password of the account associated with your EnerGyan module

	hemEmailAddr, hemPassword = module.hemEmail.getEmailLoginDetails('loginDetails.log')

	print('Sending email\n')

	module.hemEmail.sendEmail(hemEmailAddr, hemPassword, 'ychockalinga@wisc.edu', 'Power Update', str(data))

'''
def main():

	hemSuperClient.sendRequest("api/getacpoweractive/all")


if __name__ == "__main__":
    main() 
'''
