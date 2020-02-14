
servlets = ['prodarch', 'prodArchNoPXP']
logsDir = "/methode/meth01/logfiles/methode-servlets"
logFile = "em-prodarch.log"
workDir = "/methode/meth01/admin/drecheck"
tmpDir = "/tmp"

for serv in servlets:
    logToRead = "%s/%s/%s" % (logsDir, serv, logFile)
    pointerFile = "%s/.%s.pointer" % (tmpDir, serv)

    print pointerFile
