#!/usr/bin/env python3
# !/usr/bin/env python3.6 # USE THIS ON THE LOGSERVER
#https://developer.salesforce.com/docs/atlas.en-us.sfFieldRef.meta/sfFieldRef/salesforce_field_reference_Attachment.htm
import sys, os, datetime, requests, argparse
from simple_salesforce import Salesforce
import sfconfig as cfg
from tqdm import tqdm

def getAttachmentList (sf, cn):
    try:
        query = sf.query("SELECT Id, CaseNumber, (SELECT Id, Name, BodyLength, CreatedDate FROM Attachments) FROM Case where CaseNumber='%s'" % (cn))
        attachments = query['records'][0]['Attachments']['records']
    except:
        print('No attachments found at case %s' % cn)
        sys.exit(255)

    attachList = []

    for i in range(len(attachments)):
        attachList.append({
            'name':attachments[i]['Name'],
            'date':attachments[i]['CreatedDate'],
            'size':attachments[i]['BodyLength'],
            'url':attachments[i]['attributes']['url']
        })

    # Return the list of all attachments sorted by CreatedDate
    return sorted(attachList, key = lambda i: i['date'])

def downloadAttachment (attObj):

    response = requests.get('https://' + cfg.sf_instance + attObj['url'] + '/body', headers = { 'Content-Type': 'application/text', 'Authorization': 'Bearer ' + sf.session_id }, stream=True)

    filename = attObj['name']

    if os.path.isfile(filename):
        formattedCdate = datetime.datetime.strptime(attObj['date'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y%m%d%H%M%S')
        print ("File %s already exist, new filename is %s_%s" % (filename, filename, formattedCdate))
        filename = "%s_%s" % (filename, formattedCdate)

    # Download attachment using a progressbar
    pbar=tqdm(total=attObj['size'], unit='iB', unit_scale=True, desc=filename)

    with open(filename + '.uncomplete', 'wb') as fHandle:
        # 1024 is the blocksize
        for data in response.iter_content(1024):
            pbar.update(len(data))
            fHandle.write(data)
    pbar.close()
    fHandle.close

    if attObj['size'] != 0 and pbar.n != attObj['size']:
        print("ERROR, something went wrong")
    else:
        os.rename(filename+'.uncomplete',filename)

    response.close()

def downloadAll (attachsList):
    for i in range(len(attachsList)):
        downloadAttachment(attachsList[i])

def printList (theList):
    from prettytable import PrettyTable
    table = PrettyTable(['Index', 'File', 'Size (bytes)', "Created Date"])
    for i in range(len(theList)):
        table.add_row([i, theList[i]['name'],(theList[i]['size']),theList[i]['date']])
    print(table)

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="This script list all the files attached to a Salesforce case.")
    parser.add_argument("-c", "--case", metavar='Case Number' ,help="The case number. [MANDATORY]")
    parser.add_argument("-l", "--list", action='store_true', help="Only list the attachments.")
    parser.add_argument("-d", "--download", action='store_true', help="Download all the attachments without listing them")
    options = parser.parse_args(args)
    return options

options = getOptions(sys.argv[1:])

interactive = True

if options.case:
    import re
    pattern = re.compile("^\d{8}$")
    if pattern.match(options.case):
        sf = Salesforce(username= cfg.sf_user, password= cfg.sf_pass, organizationId = cfg.sf_orgid)
        myList = getAttachmentList (sf, options.case)
    else:
        print("Case number %s is wrong! \nPlease provide a proper case number" % options.case)
        sys.exit(255)
else:
    print("A case number is mandatory, please provide one")
    sys.exit(255)

if options.list:
    printList(myList)
    sys.exit(0)

if options.download:
    print("You chose to download all attachments.\nThe download will begin shortly.\n")
    downloadAll(myList)
    interactive = False

if interactive:
    printList(myList)
    exitQuestion = True
    pattern = re.compile("^(\d+(,\d+)*)?$")
    while exitQuestion:
        reply = str(input('Press [enter] or type "all" to download all attachments\nProvide a comma separated list of attachments id to download. (0,3,4 for example)\nType "exit" if you want to exit: ')).lower().strip().replace(" ", "")
        if len(reply) == 0:
            #print("pessed enter")
            downloadAll(myList)
            exitQuestion = False
        if reply.lower() == "all":
            downloadAll(myList)
            exitQuestion = False
        if pattern.match(reply):
            toDownload = reply.split(',')
            for i in toDownload:
                try:
                    downloadAttachment(myList[int(i)])
                except IndexError:
                    print("ID %s does not exist, can't download it" % i)
            exitQuestion = False
        if reply.lower() == "exit":
            print('bye!')
            exitQuestion = False



# cases
# 00023553 - no attach
# 00022690 - multiple sita
# 00016231 - chat attachments