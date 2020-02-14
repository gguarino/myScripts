#!/bin/bash

. /methode/$LOGNAME/.bash_profile


if [ $CLUSTERMODE == "ON" ] ; then
        $ADMINDIR/active.bash ${GROUP_DB} > /dev/null 2>&1
        if [ $? -eq 1 ]; then
                exit
        fi
fi

TODAY=$(date "+%Y%m%d%H%M%S")
SCRIPTLOGDIR=/methode/$LOGNAME/admin/eomdbcheck/logs

INFO=$SCRIPTLOGDIR/versant_dump.$date.log
PRCS=$SCRIPTLOGDIR/processess_dump.$date.log
TRCS=$SCRIPTLOGDIR/trace_dump.$date.log

for n in 1 2 3
do
	EOMDBLOG=$LOGDIR/eomdb$n.log
	ERRZ=$(grep -cE "SL_SEGMENT_TABLE_FULL: Shared memory segment table is full|OM_DB_NOT_FOUND: Not connected to this DB" $EOMDBLOG)
	if [ $ERRZ -gt 0 ]; then
	        ### BEGIN Collecting info for shared memory problem
        	echo "#### $DB ####" > $INFO
        	date >> $INFO;
        	echo "---- variables ----" >> $INFO
        	env | grep -e VERSANT -e ^PATH -e USER >> $INFO;
        	echo "---- shared memory usage ---- " >> $INFO
        	ipcs -am >> $INFO;
        	echo "---- VOD active databases ----" >> $INFO
        	dbtool -sys -info -activedb >> $INFO;
        	echo "---- database resources ----" >> $INFO
        	dbtool -sys -info -resource -detail $DB >> $INFO;
        	echo "---- database user mode ----" >> $INFO
        	dbinfo -p $DB >> $INFO
        	echo "---- OS memory usage ----" >> $INFO
        	free -m >> $INFO
        	# ---- other files to be collected ----
        	dbtool -trace -database $DB -view > $TRCS
        	#cp /var/log/messages $LOGDIR/.
		ps -ef > $PRCS
        	### END Collecting info for shared memory problem
	fi
done
