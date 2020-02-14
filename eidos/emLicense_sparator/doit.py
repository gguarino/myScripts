import csv, json, re
import argparse
import os.path

urlTOsend = "http://licensedumps.eidosmedia.com/emLicenseServer/service/licenses/sendreport"

def getAuth(customerId, dateToFormat, pathToEncrKey):

    # java -jar eomlicense_faker.jar CUSTOMERID dd/MM/yyyy hh:mm:ss path/to/key.pub/file
    bashCommand = "java -jar authGenerator.jar %s %s %s" % (customerId, dateToFormat, pathToEncrKey)
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    #output, error = process.communicate()

    while True:
        line = process.stdout.readline()

        authObj = re.match("CryptedAuth: (.+)", line.rstrip())
        timeStampObj = re.match("Timestamp: (.+)", line.rstrip())

        if authObj:
            authKey = authObj.group(1)

        if timeStampObj:
            timeStamp = timeStampObj.group(1)

        if line == "":
            break

    return authKey, timeStamp


parser = argparse.ArgumentParser(description='Get Info:')

parser.add_argument('-c', '--cust', help='CustomerID, eg: HTMEDIA', dest='cust')
parser.add_argument('-d', '--date', help='Date time dd/MM/yyyy hh:mm:ss, if no time is defined default will be 23:30', dest='date')
parser.add_argument('-k', '--key', help='key.pub file', dest='key')
parser.add_argument('-s', '--session', help='sessionstrace file', dest='sessions')
parser.add_argument('-u', '--users', help='userstrace file', dest='users')
args = parser.parse_args()
argCount = 0

if args.cust:
    argCount+=1
    customerID = args.cust
    print customerID

if args.date:
    argCount+=1
    dateParser = re.match("\d{2}/\d{2}/\d{4}$", args.date)
    timeStampParser = re.match("\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", args.date)
    if dateParser:
        dateToFormat = args.date + " 23:30:00"
    elif timeStampParser:
        dateToFormat = args.date
    else:
        parser.error("Unknown date format, please enter a 'dd/MM/yyyy hh:mm:ss' date")

    print dateToFormat

if args.key and os.path.isfile(args.key):
    argCount+=1
    pathToAuth = args.key
    print pathToAuth

if args.sessions and os.path.isfile(args.sessions):
    argCount+=1
    sessionsTraceFile = args.sessions
    print sessionsTraceFile

if args.users and os.path.isfile(args.users):
    argCount+=1
    usersTraceFile = args.users
    print usersTraceFile


if argCount < 5:
    argCount+=1
    parser.error("Some option is missing")



authKey, timeStamp = getAuth(customerID, dateToFormat, pathToAuth)


result = {
    "customerID": customerID,
    "authentication": authKey,
    "timestamp": timeStamp,
    "sessionTraces": [],
    "persistentTraces": []
}



with open(sessionsTraceFile, 'rb') as csvfile:
    sessionsReader = csv.reader(csvfile, delimiter=';', quotechar='|')
    counter=0
    for row in sessionsReader:
        if counter>0:
            result["sessionTraces"].append({
                "runTimestamp": row[7].replace("-",'/'),
                "sessionCreated": row[4].replace("-",'/'),
                "sessionLastModified": row[5].replace("-",'/'),
                "sessionName": row[6],
                "userName": row[3],
                "deviceId": row[1],
                "applicationId": row[0],
                "repositoryAlias": row[2],
                "privileges": []
            })
        counter = counter + 1

counter=0
with open(usersTraceFile, 'rb') as csvfile:
    usersReader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in usersReader:
        if counter>0:
            result["persistentTraces"].append({
                "runTimestamp": row[5].replace("-",'/'),
                "userName": row[3],
                "deviceId": row[1],
                "applicationId": row[0],
                "repositoryAlias": row[2],
                "lastLoginTime": row[4].replace("-",'/')
            })
        counter = counter + 1



import requests

response =  requests.post(urlTOsend, data=json.dumps(result),  headers={'Content-Type': 'application/json', 'User-Agent': 'Jakarta Commons-HttpClient/3.0.1', 'Accept': 'text/plain'})
if response.status_code != 200:
    raise ValueError(
        'Request to licenseserver returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

else:
    print response.status_code








#num_lines = sum(1 for line in open('myfile.txt'))











'''
sessions csv list positions
0 - Application id
1 - Device id
2 - Repository
3 - User name
4 - Created
5 - Last Modified
6 - Object name
7 - Run Timestamp
8 - Consumed Licenses

users csv list positions
0 - Application id
1 - Device id
2 - Repository
3 - User name
4 - Last login
5 - RunTimestamp
'''