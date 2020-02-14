import os, re
from string import Template

# Place this script in the secureCRT sessions' directory and launch it.

psmpHost = 'psmp.em.corp'
userDomainName = os.environ['USERNAME']
# if your OS is not Windows
# userDomainName = "name.surname"
rootdir = "."

tfh = open(r'session.tpl', 'rt') #open session.tpl in read and text mode
template = Template(tfh.read()) #create a template from the session.tpl file
tfh.close()

for folder, subs, files in os.walk(rootdir):
    for filename in files:
        inirex = re.search(".ini$", filename)
        if inirex:
            userName = False
            hostName = False
            with open(os.path.join(folder, filename), "r") as fh:
                lines = fh.readlines()

            for line in lines:
                userRex = re.search("S:\"Username\"=(.+)", line)
                hostRex = re.search("S:\"Hostname\"=(.+)", line)
                if userRex:
                    userName = userRex.group(1)
                    arkUsernameRex =  re.search(".+@(.+)@(.+)", line)
                    if arkUsernameRex:
                        userName = arkUsernameRex.group(1)
                        hostName = arkUsernameRex.group(2)
                if hostRex:
                    if hostRex.group(1) != psmpHost:
                        hostName = hostRex.group(1)

            if userName and hostName:
                fw = open(os.path.join(folder, filename), "w")
                # substitute the template variables
                text = template.safe_substitute(domainuser=userDomainName,
                                                targetuser=userName,
                                                hostname=hostName,
                                                psmpHost=psmpHost)
                fw.write(text.replace("\r\n", '\n'))

                fw.close()