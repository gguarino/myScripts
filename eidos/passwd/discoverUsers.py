#!/usr/bin/python
import subprocess, sys, re
import string, random

if len(sys.argv) < 3:
	print "Usage: %s database_name [action]" % sys.argv[0]
	print "\tpossible actions:"
	print "\tdisable:\tprint a list of users to disable  to input to \"eomutil users list.txt -field_spec A,N -EOMUSESER....\""
	print "\tchange_password: print a list of users and random password to input to \"eomutil users list.txt -field_spec N,K -EOMUSESER....\""
else:
	versant_db = sys.argv[1]
	action = sys.argv[2]
	if "disable" not in action and "change_password" not in action:
		print "Possible actions: \'disable\' or \'change_password\'"
		exit()

def id_generator(size=14, chars=string.ascii_uppercase + string.digits+string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

def elabora(loid, username, password, ldap, enabled):
        if enabled == "" and password == "" and ldap == "":
		if action == "disable":
                	print "D;%s" % username
		if action == "change_password":
			print "%s:%s" % (username,id_generator())


cmd = ["db2tty", "-D", versant_db, "-i", "EOM_User_p"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
loid = False
for line in proc.stdout.readlines():
        uRex = re.match(".+EOM_Object_p::name_.*=\"(.+)\"", line)
        if uRex:
                username = uRex.group(1)

        pRex = re.match(".+EOM_User_p::password_.*=\"(.*)\"", line)
        if pRex:
                password = pRex.group(1)

        lRex = re.match(".+EOM_User_p::ldap_setting_.*=\"(.*)\"", line)
        if lRex:
                ldap = lRex.group(1)

        enabRex = re.match(".+EOM_User_p::account_disabled_.*=\"(.*)\"", line)
        if enabRex:
                enabled = enabRex.group(1)

        ### L {=0x7ff0a77fece0;c_l_();;0} #0x7ff0a77fece0[1.0.199128948:EOM_User_p]  T=0x7ff0a76fa568 {reg} (meth01)


        startUserRex = re.match("^## L.+\[(\d+\.\d+.\d+):EOM_User_p\]", line)
        if startUserRex:
                if loid:
                    elabora(loid, username, password, ldap, enabled)
                    username = ""
                    password = ""
                    ldap = ""
                    enabled = ""
                loid = startUserRex.group(1)

        endFileRex = re.match("^\*\*\*\*\*\* Total", line)
        if endFileRex:
                elabora(loid, username, password, ldap, enabled)				

				
#eomutil users userchange -field_spec N,K -EOMUser Admin -EOMPassword syseidospwd -EOMRepositoryIor $IORDIR/eomdb1.io				
