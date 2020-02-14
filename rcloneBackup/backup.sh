#!/usr/bin/env bash

DBUSR=$(grep DB_USER /opt/www-cso/wp-config.php | cut -d"'" -f4)
PSWD=$(grep DB_PASSWORD /opt/www-cso/wp-config.php | cut -d"'" -f4)

WORKDIR=/opt/backup/cso
TODAY=$(date +"%Y%m%d")
AMONTHAGO=$(date +"%Y%m%d" -d "now - 30 days")
BCKDIR=${WORKDIR}/${TODAY}
SQLDUMP=${BCKDIR}/csosite_dump.sql

mkdir -p ${BCKDIR}

echo "Dumping"
/bin/mysqldump -u ${DBUSR} -p${PSWD} --database cso > ${SQLDUMP} 2>/dev/null
/bin/gzip ${SQLDUMP}

echo "Tarring"
/bin/tar czf ${BCKDIR}/cso_www_root.tar.gz /opt/www-cso > /dev/null 2>&1

echo "Uploading today"
/bin/rclone mkdir cso:backup/${TODAY}
/bin/rclone copy ${BCKDIR} cso:backup/${TODAY}

echo "Deleting 1 month-old backup"
/bin/rclone purge --drive-use-trash=false cso:backup/${AMONTHAGO}

rm -fr ${BCKDIR}