#!/usr/bin/env python3
from datetime import datetime
from operator import itemgetter
import random

def randomTimeGen(start, end):
    # Calculate a random time between 9:00:00 and 11:59:59
    result = start + random.random() * (end - start)
    return str(result.strftime("%H:%M:%S"))

def randomPIDGen():
    return str(random.randrange(3000, 5000))

def downloadRawText(theURL):
    # This is the ugliest function in this script, because of the many assignments of "line" variable.
    import urllib.request
    import re

    theURL = "%s%s" % (wikiURL, "?action=raw") 
    data = urllib.request.urlopen(theURL)
    listToReturn = []
    for line in data:
        # Split line by dot and remove all <ref> tags and content
        line = line.decode('utf-8').replace("\.", ".\n").replace("</ref>", "\n")
        line = re.sub("<ref.*", "", line)
        line = re.sub("\[|\]", "", line) # remove all square brackets
        line = re.sub("\{[^\}]*\}", "", line) # remove all braces
        line = line.replace("|", "/") # replace all pipes with a slash, to avoid to add some extra pipes to my output
        for splitline in line.split("\n"):
            if re.match("^[a-zA-Z0-9]", splitline):
                listToReturn.append(splitline)

    return listToReturn

def randomDataSelector(myList):
    # Given a list in input this function will choose randomly an item
    return myList[random.randrange(len(myList))]

def addComment(lineList, maxLen):
    theLine = "|".join(lineList)
    if len(theLine) > maxLen:
        # If the line is longer than 480 chars I trim it in order to have at least 20 free chars to add a comment.
        theLine = theLine[:maxLen - 20]
    # Calculating how many X I need to add to have a 500byte line.
    # Last "-2" is due to the final pipe to add and the carriage return.
    commentLen = maxLen - len(theLine) - 2
    return "%s|%s\n" % (theLine, 'X' * commentLen)

wikiURL = "https://en.wikipedia.org/wiki/Amazon_S3"
today = str(datetime.now().strftime("%Y%m%d"))
startTime = datetime.strptime('09:00:00', '%H:%M:%S')
endTime = datetime.strptime('11:59:59', '%H:%M:%S')
maxStringLen=500
lines = 10000
logFile = "random.log"

sentences = downloadRawText(wikiURL)
logsList = []

# I generate a first list that contains all requested data except the comment
for lineNumber in range(lines):
    logsList.append([today, randomTimeGen(startTime, endTime), randomPIDGen(), randomDataSelector(["OK", "TEMP", "PERM"]), randomDataSelector(sentences)])

fileWriter = open(logFile, "w")
# Data contained in the list is not sorted
# Sorting the array by date (second item), in this way the log will be credible
for line in sorted(logsList, key=itemgetter(1)):
    fileWriter.write(addComment(line, maxStringLen))
fileWriter.close()

print("All done, the logfile %s has been created" % logFile)