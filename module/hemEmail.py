# 
# This module is used to send email 

# Author: Ashray Manur

import smtplib

def sendEmail(userEmail, userPassword, destinationEmail, emailSubject, emailBody):
	dest_email = destinationEmail
	user_email = userEmail
	user_password = userPassword
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(user_email, user_password)
	if(emailSubject==''):
		emailSubject = 'HEM'
	header = 'To:' + dest_email + '\n' + 'From: ' + user_email + '\n' + 'Subject: ' + emailSubject +'\n'
	totalMessage = header + emailBody
	smtpserver.sendmail(user_email, dest_email, totalMessage)
	print('Email sent\n')
	smtpserver.close()
	return 


def getEmailLoginDetails(fileName):

	fh = open(fileName, 'r')

	for i, line in enumerate(fh):
		data = line.split(":")
		if(data[0] == 'email'):
			address = data[1]
			address = address.rsplit("\n" , 1)[0]
		if(data[0] == 'password'):
			password = data[1]

	return address, password