import os, re

# Place this script in the secureCRT sessions' directory and launch it.

rootdir = "."

fw = open(os.path.join(rootdir+".csv"), "w")

fw.write("Password_name,Safe,Folder,Password,DeviceType,PolicyID,Address,UserName,CPMDisabled,ResetImmediately\n")


for folder, subs, files in os.walk(rootdir):

    # print folder
    for filename in files:
        inirex = re.search("__FolderData__.*", filename)
        if not inirex:
            #print folder+"\\"+filename
            userName = False
            hostName = False
            with open(os.path.join(folder, filename), "r") as fh:
                lines = fh.readlines()
            fh.close()

            for line in lines:
                userRex = re.search("S:\"Username\"=(.+)", line)
                hostRex = re.search("S:\"Hostname\"=(.+)", line)
                if userRex:
                    userName = userRex.group(1)
                if hostRex:
                    hostName = hostRex.group(1)

            #print "%s\\%s,%s,%s" % (folder, filename[:-4], userName, hostName)


            fw.write("%s,%s,Root\\%s,%s,Operating System,Policy_UnixSSH_NO_CPM,%s,%s,NO_VALUE,\n" % (filename[:-4], rootdir, folder, userName, hostName, userName))


fw.close()