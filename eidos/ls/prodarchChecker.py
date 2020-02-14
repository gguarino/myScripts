#!/usr/bin/python
import os, sys, re
from datetime import datetime

def getPointer(pointerFile):
    try:
        po = open(pointerFile, "r")
        pointer = int(po.readline())
        po.close()
    except IOError:
        # Nessun puntatore, parto da zero
        pointer = 0

    return pointer

def setPointer(pointerFile, pointer):
    po = open(pointerFile, "w+")
    po.seek(0)
    po.write(str(pointer))
    # po.truncate()
    po.close()

def getFileSize(logfile):
    try:
        filesize = os.stat(logfile).st_size
    except OSError:
        sys.stdout.write(logfile + ": No such file or directory\n")
    return filesize

def sendMail(servlet, TEXT):
    import smtplib, socket
    from email import MIMEText

    hostname = socket.gethostname()

    FROM = 'meth01@' + hostname
    TO = ['giuseppe.guarino@eidosmedia.com']

    # Create a text/plain message
    msg = MIMEText(TEXT)

    msg['Subject'] = "[LS] "+servlet+" Prodarch Bloccata"
    msg['From'] = FROM
    msg['To'] = ";".join(TO)

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(FROM, TO, msg.as_string())
    print "Successfully sent email"

sys.stdout.write("-------------- " + str(datetime.now()) + " --------------\n")

servlets = ['prodArch', 'prodArchNoPXP']
logsDir = "/methode/meth01/logfiles/methode-servlets"
logFile = "em-prodarch.log"
workDir = "/methode/meth01/admin/drecheck"
tmpDir = "/tmp"

for serv in servlets:

    logToRead = "%s/%s/%s" % (logsDir, serv, logFile)

    filesize = getFileSize(logToRead)
    pointerFile = "%s/.%s.pointer" % (tmpDir, serv)
    pointer = getPointer(pointerFile)

    sys.stdout.write("Servlet: " + serv + " POINTER: " + str(pointer) + " FILESIZE: " + str(filesize) + " - ")

    if pointer == filesize:
        sys.stdout.write("No new lines, no read\n")
        continue
    elif pointer > filesize:
        sys.stdout.write("Rotated\n")
        pointer = 0
    else:
        sys.stdout.write("Keep reading\n")

    alarm = False

    fh = open(logToRead, "r")
    fh.seek(pointer)
    for line in fh:
        pointer += len(line)
        elapsedRex = re.search("older session's elapsed seconds:\s+([0-9]+),", line)
        if elapsedRex and int(elapsedRex.group(1)) >= 600:
            alarm = True
    fh.close()
    setPointer(pointerFile, pointer)

    if alarm:
        sendMail(serv, "La prodArch risulta bloccata, per favore riavvia il tomcat-tools")

sys.stdout.write("\n")