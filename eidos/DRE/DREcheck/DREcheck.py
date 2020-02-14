#!/usr/bin/python
import os, sys

def getPointer(pointerFile):
	try:
		po = open(pointerFile, "r")
		pointer =int(po.readline())
		po.close()
	except IOError:
		# Nessun puntatore, parto da zero
		pointer = 0
		
	return pointer

def setPointer(pointerFile, pointer):
	po = open(pointerFile, "w+")
	po.seek(0)
	po.write(str(pointer))
	#po.truncate()
	po.close()	

def getFileSize(logfile):
	try:
		filesize = os.stat(logfile).st_size
	except OSError:
		sys.stdout.write(logfile+": No such file or directory\n")
	return filesize

def sendMail(DRE, TEXT):
	import smtplib
	from email.mime.text import MIMEText

	FROM = 'DRECheck@godo.meth02'
	TO = ['giuseppe.guarino@eidosmedia.com']
	
	# Create a text/plain message
	msg = MIMEText(TEXT)

	msg['Subject'] = "[GODO] Troubles founded on DRE"+str(DRE)
	msg['From'] = FROM
	msg['To'] = ";".join(TO) 

	smtpObj = smtplib.SMTP('localhost')
	smtpObj.sendmail(FROM, TO, msg.as_string())         
	print "Successfully sent email"

autonomies = [1,2,3,4,5,6,7,8,9]
lista = ["Unable to read", "File I/O error", "No such file or directory", "Unable to read"]
workDir = "/methode/meth02/admin/drecheck/"
tmpDir = "/tmp/"

for n in autonomies:
	found = False
	mailMessage = ""
	logfile = "/methode/meth02/logfiles/autonomy/DRE"+str(n)+"/application.log"
	filesize = getFileSize(logfile)
	pointerFile = tmpDir+os.path.basename(logfile)+str(n)+".pointer"
	pointer = getPointer(pointerFile)

	sys.stdout.write("DRE"+str(n)+" - POINTER: "+str(pointer)+" FILESIZE: "+str(filesize)+" - ")

	if pointer == filesize:
		sys.stdout.write("No new lines, no read\n")
		continue
	elif pointer > filesize:
		sys.stdout.write("Rotated\n")
		pointer = 0
	
	sys.stdout.write("Reading "+logfile+"\n")
	fh = open(logfile, "r")
	fh.seek(pointer)
	for line in fh:
		pointer += len(line)
		if any(word in line for word in lista):
			found = True
			mailMessage += line
	fh.close()
	setPointer(pointerFile, pointer)

	if found:
		sys.stdout.write("Sending email for DRE"+str(n)+"\n")
		sendMail(n, mailMessage)