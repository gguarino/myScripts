import os, re, tornado.web
from tornado.options import options
from utils.transmission import Transmission

class usbHandler(tornado.web.RequestHandler):
    
    def get(self):
        devices = [ ]
        in_file = open("/etc/mtab","r")
        rex = re.compile('\/dev\/sd[b-z]')
        noUsbDevices = True
        for line in in_file:
            if rex.match(line):
                noUsbDevices = False
                fields = line.split( )
                mounted = self.isMounted(options.transmission_dload_dir, fields[1])
                devices.append ([fields[0], fields[1], mounted])
        in_file.close()

        if noUsbDevices:
            self.write("No USB Devices Found!")
        else:
            trans = Transmission(options.transmission_app)
            self.render("usb.html", devices=devices, trans=trans)
            
            #for idx, device in enumerate(devices):
                #self.write(device[0]+" "+device[1])
    def isMounted(self,symlink,realpath):
        if os.path.islink(symlink) and os.path.realpath(symlink) == realpath:
            return 1
        else:
            return 0
