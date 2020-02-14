#!/usr/bin/python
import os, sys, re
import paramiko
import socket
import subprocess
import urllib2

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

def sendMail(TEXT):
    import smtplib
    from email.mime.text import MIMEText

    FROM = 'methcms@'+socket.gethostname()
    TO = ['someone@example.com']
    # Create a text/plain message
    msg = MIMEText(TEXT)

    msg['Subject'] = "[CMG] Error InvalidType on " + os.environ["SILOS_NAME"]
    msg['From'] = FROM
    msg['To'] = ";".join(TO)

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(FROM, TO, msg.as_string())
    print "Successfully sent email"

def run_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return {"stdout": stdout, "stderr": stderr}

def getPathSSH (loid):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(coreHost, username="methcms", password="methcms")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(". .bash_profile; /methode/methcms/bin/eomutil info %s -path $CONN" % loid)
        return ssh_stdout.readlines()[0]

    except:
        return "SSH ERROR"


webcacheUrl = sys.argv[1]
logfile = "/methode/methcms/logfiles/alertcache/alertcache.log"
errorToFind = "InvalidType:1.0"
tmpDir = "/tmp/"

coreHost=socket.gethostbyname(os.environ['GROUP_CORE'])
filesize = getFileSize(logfile)
pointerFile = tmpDir + "." + os.path.basename(logfile) + ".pointer"
pointer = getPointer(pointerFile)

sys.stdout.write("POINTER: "+str(pointer)+" FILESIZE: "+str(filesize)+" - ")

if pointer == filesize:
    sys.stdout.write("No new lines, no read\n")
    exit()
elif pointer > filesize:
    sys.stdout.write("Rotated\n")
    pointer = 0

sys.stdout.write("Reading "+logfile+"\n")
fh = open(logfile, "r")
fh.seek(pointer)

message = ""
oldPrevious = ""
previousLine = ""
found = False
mailMessage = ""

invalidQueries = {}

for line in fh:
    if errorToFind in line:
        # FOUND!
        loidRex = re.match(".+query (\d+\.\d+\.\d+) error", previousLine)
        if loidRex:
            found = True
            loid = loidRex.group(1)
            timeRex = re.match("(\d+ \d{2}:\d{2}:\d{2}).+", oldPrevious)
            if timeRex:
                errorTime = timeRex.group(1)
            else:
                errorTime = "NOTIME"

            invalidQueries[loid] = errorTime

    else:
        oldPrevious = previousLine
        previousLine = line

    pointer += len(line)
fh.close()
setPointer(pointerFile, pointer)

if found:

    for loid,timeSta in invalidQueries.items():
        print "Working on "+loid
        command = "java -cp /methode/methcms/tools/AlertQueryFixer/alert-query-fixer.jar:lib/* com.eidosmedia.us.cmg.util.AlertQueryFixer %s %s" % (loid, os.environ['CONN'])
        cmdRet = run_command(command)
        print cmdRet['stdout']
        urlToGet = "http://%s:9601/debug/utils/alertcache.jsp?action=reload&id=%s" % (webcacheUrl, loid)
        errMess = "FIXED!"

        try:
            response = urllib2.urlopen(urlToGet, timeout=5)
            html = response.read()
        except urllib2.URLError, e:
            errMess = "TIMEOUTS"

        # java -cp alert-query-fixer.jar:lib/* com.eidosmedia.us.cmg.util.AlertQueryFixer 2.0.210326730 $CONN

        # curl http://ausv1apl-digwc01.em-cmg.ausv.int:9601/debug/utils/alertcache.jsp?action=reload&id=2.0.210326730


        queryPath = getPathSSH(loid)
        thisError = "%s - %s - %s - %s\n" % (errorTime, loid, queryPath, errMess)
        message = message + thisError

    sys.stdout.write("Sending email\n")
    sendMail(message)
    print message

'''
            #eomutil info 2.0.210336178 -path $CONN
            # ssh methcms@AUSV1APL-DIGCORE01 ". .bash_profile; /methode/methcms/bin/eomutil info 2.0.210336178 -path $CONN
'''