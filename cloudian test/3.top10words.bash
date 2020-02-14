#!/bin/bash

LOGFILE=random.log
OUTPUTFILE=top10words.txt


cut -d'|' -f5 $LOGFILE | tr ' ' '\n' | sort | uniq -c | sort -nr | head -10 > $OUTPUTFILE