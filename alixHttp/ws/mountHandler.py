import tornado.web, os
from tornado.options import options
from utils.transmission import Transmission

class mountHandler(tornado.web.RequestHandler):
    def post(self):
        action=self.get_argument("submit", default=None, strip=False)
        dev=self.get_argument("device", default=None, strip=False).split( ) # 0 = mountpoint , 1 = directory mount
        
        trans = Transmission(options.transmission_app)
        
        if action == "Monta":
            if trans.isUp():
                trans.letDaemon('stop')
                if trans.getRetCode() != 0:
                    self.write("Transmission cannot be stopped: "+trans.getErr())
                    exit()
            if os.path.isdir(options.transmission_dload_dir) and os.path.islink(options.transmission_dload_dir):
                self.write("/mnt/P2P-HD is already mounted")
                self.write("<a href=/usb>Go Back!</a>")
                # self.redirect(u"/usb")
                if not trans.isUp():
                    trans.letDaemon('start')
                    if trans.getRetCode() != 0:
                        self.write("Transmission is down but cannot be started: "+trans.getErr())
                        self.write("<a href=/usb>Go Back!</a>")
                        exit()
            else:
                self.write("Crea link simbolico -> ln -s "+dev[1]+" "+ options.transmission_dload_dir + "<br>")
                os.system("ln -s "+dev[1]+" "+ options.transmission_dload_dir) # Se esiste?
                self.write("Start di transmission <br>")
                trans.letDaemon('start')
                if trans.getRetCode() != 0:
                    self.write("Transmission cannot be started: "+trans.getErr())
                    self.write("<a href=/usb>Go Back!</a>")
                    exit()
                self.write("<a href=/usb>Go Back!</a>")
        elif action == "Smonta":
            self.write("Spegni Transmission<br>")
            trans.letDaemon('stop')
            if trans.getRetCode() != 0:
                self.write("Transmission cannot be stopped: "+trans.getErr())
                self.write("<a href=/usb>Go Back!</a>")
                exit()
            self.write("Rimuovi link simbolico -> rm "+options.transmission_dload_dir+"<br>")
            os.system("rm "+options.transmission_dload_dir)
            self.write("<a href=/usb>Go Back!</a>")
        else:
            if trans.isUp():
                trans.letDaemon('stop')
                if trans.getRetCode() != 0:
                    self.write("Transmission cannot be stopped: "+trans.getErr())
                    exit()
            self.write("Umount "+dev[1]+ "<br>")
            os.system("umount "+dev[1])
            self.write("<a href=/usb>Go Back!</a>")

    def get(self):
        self.write("Cazzo Vuoi")