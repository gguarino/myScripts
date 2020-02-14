#!/bin/bash

FILENAME="/methode/meth01/logfiles/autonomy/DRE2/query.log"
DATE=$(date +%d%m%Y)

ABANCOUNT=$(grep -c Abandoning $FILENAME)
LASTAPPLINE="/tmp/dre2check.$DATE"

APPLOG="/methode/meth01/logfiles/autonomy/DRE2/application.log"

if [ $ABANCOUNT -gt 1 ]; then
echo $ABANCOUNT
if [ ! -e $LASTAPPLINE ]; then
tail -1 $APPLOG > $LASTAPPLINE
# echo "qua"
else
LASTLI=$(tail -1 $APPLOG)

# echo $LASTLI
# cat $LASTAPPLINE

if [ "$LASTLI" == "$(cat $LASTAPPLINE)" ]; then
echo "DRE2 da riavviare" | mail -s "Riavvia DRE" giuseppe.guarino@eidosmedia.com
echo "MANDOLAMAIL"
fi
echo $LASTLI > $LASTAPPLINE
fi

fi