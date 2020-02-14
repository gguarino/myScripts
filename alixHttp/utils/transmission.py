import subprocess
class Transmission():
    
    trans_app_name = ""
    std_output = ""
    std_err = ""
    ret_code = 9999
    pid = ""
    
    def __init__(self,trans_app_name):
        self.trans_app_name = trans_app_name
    
    def isUp(self):
        self.pid = subprocess.Popen(['pidof', self.trans_app_name], stdout=subprocess.PIPE).communicate()[0]
        if self.pid == "":
            return False
        return True
    
    def letDaemon(self, startstop):
        cmd = subprocess.Popen(["/etc/init.d/"+self.trans_app_name, startstop], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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