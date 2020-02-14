import subprocess
import os
class SvcManager():
    service_name = ""
    std_output = ""
    std_err = ""
    ret_code = 9999
    pid = ""
    
    def __init__(self,service_name):
        self.service_name = service_name
    
    def isUp(self):
        self.pid = subprocess.Popen(['pidof', self.service_name], stdout=subprocess.PIPE).communicate()[0]
        if self.pid == "":
            return False
        return True
    
    def letService(self, startstop):
	cmd = subprocess.Popen(["/etc/init.d/"+self.service_name, startstop.lower()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        std = cmd.communicate()
        self.std_output = std[0]
        self.std_err = std[1]
        self.ret_code = cmd.returncode
        return
    
    def getPid(self):
        return self.pid
    
    def getOutput(self):
        return self.std_output
    
    def getErr(self):
        return self.std_err
        
    def getRetCode(self):
        return self.ret_code
        
    def getName(self):
        return self.service_name
