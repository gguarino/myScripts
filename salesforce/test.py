#!/usr/bin/env python3



'''
CaseFeed attachments
SELECT Body,CreatedDate,Id,LastModifiedDate, LinkUrl,ParentId,RelatedRecordId,SystemModstamp,Title,Type,Visibility FROM CaseFeed WHERE ParentId = '5005F000010coqZQAQ' and Type = 'ContentPost' ORDER BY CreatedDate DESC NULLS FIRST LIMIT 10

IMPROVE

https://github.com/ysfdc/salesforce_scripts/blob/master/attachments_downloader.py

'''
#!/usr/bin/env python3
# !/usr/bin/env python3.6 # USE THIS ON THE LOGSERVER
#https://developer.salesforce.com/docs/atlas.en-us.sfFieldRef.meta/sfFieldRef/salesforce_field_reference_Attachment.htm
import sys, os, datetime, requests, argparse
from simple_salesforce import Salesforce
import sfconfig as cfg
from tqdm import tqdm

def getAttachSize (url):

    print('https://' + cfg.sf_instance + url )
    #response = requests.get('https://' + cfg.sf_instance + url + '/describe', headers = { 'Content-Type': 'application/text', 'Authorization': 'Bearer ' + sf.session_id }, stream=True)

    #print(response)



def getAttachmentList (sf, cn):

    caseQuery = sf.query("SELECT Id, CaseNumber, (SELECT Id, Name, BodyLength, CreatedDate FROM Attachments) FROM Case where CaseNumber='%s'" % (cn))

    try:
        caseId = caseQuery['records'][0]['Id']
    except:
        print('Case %s does not exist' % cn)
        sys.exit(255)

    attachList = []

    if (caseQuery['records'][0]['Attachments'] is not None ):

        caseAttachments = caseQuery['records'][0]['Attachments']['records']
        for i in range(len(caseAttachments)):
            print(caseAttachments[i]['attributes']['url'])
            attachList.append({
                'name':caseAttachments[i]['Name'],
                'date':caseAttachments[i]['CreatedDate'],
                'size':caseAttachments[i]['BodyLength'],
                'url':caseAttachments[i]['attributes']['url'] + '/body'
            })



    caseFeedQuery =  sf.query("SELECT Id,Title,CreatedDate FROM CaseFeed where Type='ContentPost' AND ParentId='%s'" % caseId)
    caseFeedAttachments = caseFeedQuery['records']
    print(caseFeedAttachments)

    caseFeedQuery2 =  sf.query("SELECT Body, (SELECT RecordId, Title, Type, Value FROM FeedAttachments) FROM FeedItem WHERE Id='0D55F00008s95MlSAI'")
    print(caseFeedQuery2)
    exit()
    if len(caseFeedAttachments) > 0:

        for i in range(len(caseFeedAttachments)):


            peppeQuery =  sf.query("SELECT Id FROM FeedAttachment WHERE FeedEntityId = '%s'" % caseFeedAttachments[i]['Id'])

            print(peppeQuery['records'][0]['attributes']['url'])

            attachList.append({
                'name':caseFeedAttachments[i]['Title'],
                'date':caseFeedAttachments[i]['CreatedDate'],
                'size':0,
                'url':peppeQuery['records'][0]['attributes']['url']
            })


    if len(attachList) == 0:
        print('No attachments found at case %s' % cn)
        sys.exit(255)
    else:
        # Return the list of all attachments sorted by CreatedDate
        return sorted(attachList, key = lambda i: i['date'])

def downloadAttachment (attObj):

    response = requests.get('https://' + cfg.sf_instance + attObj['url'], headers = { 'Content-Type': 'application/text', 'Authorization': 'Bearer ' + sf.session_id }, stream=True)

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

sf = Salesforce(username= cfg.sf_user, password= cfg.sf_pass, organizationId = cfg.sf_orgid)
myList = getAttachmentList (sf, '00016231')

#print(myList)

printList(myList)
#downloadAll(myList)

# cases
# 00023553 - no attach
# 00022690 - multiple sita
# 00016231 - chat attachments