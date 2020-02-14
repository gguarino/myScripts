#!/usr/bin/python
import os, sys, re, urllib2
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

def dreStucked(dreURL):
    try:
        response = urllib2.urlopen(dreURL, timeout=5)
        response.read()
    except urllib2.URLError, e:
        return True

    return False


def sendMail(DRE, TEXT):
    import smtplib
    from email.mime.text import MIMEText

    FROM = 'meth01@AUSV1APL-EDISEARCH01.em-cmg.ausv.int'
    TO = ['giuseppe.guarino@eidosmedia.com']

    # Create a text/plain message
    msg = MIMEText(TEXT)

    msg['Subject'] = "[CMG] Restart DRE" + str(DRE)
    msg['From'] = FROM
    msg['To'] = ";".join(TO)

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(FROM, TO, msg.as_string())
    print "Successfully sent email"


sys.stdout.write("-------------- " + str(datetime.now()) + " --------------\n")

autonomies = [2]
logsDir = "/methode/meth01/logfiles/autonomy/DRE"
workDir = "/methode/meth01/admin/drecheck/"
tmpDir = "/tmp/"

for n in autonomies:
    queryLog = "%s%s/query.log" % (logsDir, n)
    appLog = "%s%s/application.log" % (logsDir, n)
    indexLog = "%s%s/index.log" % (logsDir, n)

    sys.stdout.write("Reading " + indexLog + "\n")
    # 1 e' finita la compact?
    compactFinished = False
    idxfh = open(indexLog, "r")
    for line in idxfh:
        if "Stage: Z (Finish Compaction)" in line:
            # 06/07/2017 03:35:30 [1] 30-Normal: Stage: Z (Finish Compaction), Time: 0 seconds
            timeRex = re.match("(\d{2}\/\d{2}\/\d{4}) (\d{2}:\d{2}:\d{2}).+", line)
            if timeRex:
                if timeRex.group(1) == datetime.now().strftime('%d/%m/%Y'):
                    compactFinished = True
                    sys.stdout.write("Compact finished " + timeRex.group(1) +" "+ timeRex.group(2) + "\n")
    idxfh.close()

    if compactFinished:

        if dreStucked("http://%s:%s/?action=getstatus" % (os.environ['GROUP_SEARCH'], os.environ["DRE"+str(n)+"_PORT"]) ):
            sendMail(n, "Il DRE"+str(n)+" non risponde... riavviareeee")
            sys.stdout.write("DRE" + str(n) + " stucked! Sending email and exit ")
            exit(255)
        else:
            sys.stdout.write("DRE" + str(n) + " is responsive \n")

        # conta occorrenze di "Abandoning query"
        filesize = getFileSize(queryLog)
        pointerFile = tmpDir + os.path.basename(queryLog) + str(n) + ".pointer"
        pointer = getPointer(pointerFile)

        sys.stdout.write("DRE" + str(n) + " query.log - POINTER: " + str(pointer) + " FILESIZE: " + str(filesize) + " - ")

        if pointer == filesize:
            sys.stdout.write("No new lines, no read\n")
            continue
        elif pointer > filesize:
            sys.stdout.write("Rotated\n")
            pointer = 0
        else:
            sys.stdout.write("Keep reading\n")

        abandonCount = 0

        fh = open(queryLog, "r")
        fh.seek(pointer)
        for line in fh:
            pointer += len(line)
            if "Abandoning query" in line:
                abandonCount += 1
        fh.close()
        setPointer(pointerFile, pointer)

        if abandonCount > 1:
            sys.stdout.write(str(abandonCount)+" abandoning queries in 5 minutes\n")
            appfh = open(appLog, "r")
            for line in appfh:
                lastLine = line
            appfh.close()

            if "Writing out stateinfo" in lastLine:
                stateRex = re.match("(\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}).+", line)
                if stateRex:
                    stateTime = datetime.strptime(stateRex.group(1), '%d/%m/%Y %H:%M:%S')
                    delta = datetime.now() - stateTime
                    if delta.seconds > 300:
                        sys.stdout.write("DRE stuck, sending email!!\n")
                        sendMail(n, "Sono state trovate "+str(abandonCount)+" abandoning queries e application.log non si aggiorna da "+str(delta.seconds)+" secondi\n RIAVVIARE IL DRE"+str(n))
        else:
            sys.stdout.write("No Abandoning queries found\n")
    else:
        sys.stdout.write("Compact Still running\n")

sys.stdout.write("\n")