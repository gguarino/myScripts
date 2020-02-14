#!/usr/bin/python
import os
import sys
import paramiko
import socket
import subprocess

def run_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return {"stdout": stdout, "stderr": stderr}

def cleanAlertSSH (ssh_host, urlT):
    ssh_host = socket.gethostbyname(ssh_host)
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(ssh_host, username="methpt", password="methpt")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("curl %s" % urlT)
        return ssh_stdout.readlines()
    except:
        return "Unexpected error:", sys.exc_info()[0]


loidList = sys.argv[1]

if not os.path.exists(loidList):
    print "File %s does not exist" % loidList
    exit()

fh = open(loidList, "r")
for loid in fh:
    comand = "java -cp /methode/methcms/tools/AlertQueryFixer/alert-query-fixer.jar:lib/* com.eidosmedia.us.cmg.util.AlertQueryFixer %s $CONN " % ''.join(loid.splitlines())

    cmdRet = run_command(comand)

    print cmdRet['stdout']

    urlToGet = "http://localhost:9601/debug/utils/alertcache.jsp?action=reload&id=%s" % loid
    print urlToGet
    ret = cleanAlertSSH("AUSV1BSTGL-DIGWC06", urlToGet)
    print ret