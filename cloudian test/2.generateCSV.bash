#!/bin/bash

LOGFILE=random.log
CSV=intermediate.csv

cut -d'|' -f2,4  $LOGFILE | tr "|" ","  | tr ":" "," > $CSV