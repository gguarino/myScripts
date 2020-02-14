import re, time


def parseDate(date):
    struct_time = time.strptime(date, "%b %d %H:%M:%S %Y")
    return "%02d/%02d/%s %02d:%02d:%02d" % (struct_time.tm_mday,struct_time.tm_mon,struct_time.tm_year,struct_time.tm_hour,struct_time.tm_min,struct_time.tm_sec)

endFlag = False



out_file = open("report.csv","w")
out_file.write("Customer,date,partial,total\n")

with open("dbclean.txt") as f:
    for line in f:
        customerRe = re.search("\[(.+)\].+", line)
        if customerRe:
            customer = customerRe.group(1)
        startRe = re.search("The process ended.+[A-Za-z]{3} ([A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2}) CET (\d{4})", line)
        if startRe:
            endFlag = True
            cleandate = parseDate(startRe.group(1)+" "+startRe.group(2))


        if endFlag:
            processed = re.search("Elements processed in this execution:\s+(.*)", line)
            if processed:
                partial_proc = processed.group(1).replace(",", "")
            pun = re.search("Elements processed until now:\s+(.*)", line)
            if pun:
                total_proc = pun.group(1).replace(",", "")
                out_file.write("%s,%s,%s,%s\n" % (customer,cleandate,partial_proc,total_proc))

                endFlag = False

out_file.close()