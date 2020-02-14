#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import boto3, re

# author:           Giuseppe Guarino
# date:                 27/04/2018
# descritpion:      This simple rest reserver returns all the dynamic IPs for the desired Autoscaling Group

PORT_NUMBER = 20090


def getInstancesIP(desiredASgroup):
    ec2 = boto3.resource('ec2')
    client = boto3.client('autoscaling')
    paginator = client.get_paginator('describe_auto_scaling_groups')
    groups = paginator.paginate().build_full_result()

    for asg in groups['AutoScalingGroups']:
        if desiredASgroup in asg['AutoScalingGroupName']:
            #print asg['AutoScalingGroupName']
            instance_ids = [inst['InstanceId'] for inst in asg['Instances']]
            running_instances = ec2.instances.filter(Filters=[{}])
            for instance in running_instances:
                if instance.id in instance_ids:
                    yield instance.private_ip_address

def getASGroups():
    ec2 = boto3.resource('ec2')
    client = boto3.client('autoscaling')
    paginator = client.get_paginator('describe_auto_scaling_groups')
    groups = paginator.paginate().build_full_result()

    for asg in groups['AutoScalingGroups']:
        yield asg['AutoScalingGroupName']

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def ok(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):

        asgroups = re.search("\/asg.*", self.path)
        silorex = re.search("\/wc\/(\d-\d{3}|\d).*", self.path)
        if asgroups:
            results = getASGroups()
            self.ok()
            for asg in results:
                self.wfile.write(asg+"\n")
        elif silorex:
            inputAS = "AUSV1PL-DIGWC0%s" % silorex.group(1)
            results = getInstancesIP(inputAS)
            self.ok()
            for ip in results:
                self.wfile.write(ip+"\n")
        else:
            self.send_response(404)
            self.wfile.write("Wrong Request")
        return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()