#!/usr/bin/python

logfile="DREcheck.py"
fh = open(logfile, "r")
for line in fh:
   lastline=line
fh.close()

print lastline