import tornado.web
from utils.svcmanager import SvcManager

class daemonHandler(tornado.web.RequestHandler):

    sn = ['transmission-deamon', 'minidlna', 'ssh']
    services = []

    def initialize(self):
        if (len(self.sn) > len(self.services)) :
            for name in self.sn:
                service = SvcManager(name)
                self.services.append(service)

    def get(self):
        self.render("daemons.html", services=self.services)

    def post(self):
        servname=SvcManager(self.get_argument("servname", default=None, strip=False))
        action=self.get_argument("action", default='stop', strip=False)

        servname.letService(action)

        self.render("daemons.html", services=self.services)