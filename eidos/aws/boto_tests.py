import boto3, re

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
                    yield instance

def getASGroups():
    ec2 = boto3.resource('ec2')
    client = boto3.client('autoscaling')
    paginator = client.get_paginator('describe_auto_scaling_groups')
    groups = paginator.paginate().build_full_result()

    for asg in groups['AutoScalingGroups']:
        yield asg['AutoScalingGroupName']

asgroups = getASGroups()
for asg in asgroups:
    print asg

#result=getInstancesIP("AUSV1PL-DIGWC01")
#for inst in result:
#    print inst.private_ip_address


