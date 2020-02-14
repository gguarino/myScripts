#!/usr/bin/env bash

SCRIPTDIR=$(dirname $0)

source ${SCRIPTDIR}/slackAway.conf > /dev/null 2>&1

case "${1}" in
    away)
        presence='away'
        ;;
    here)
        presence='auto'
        ;;
    get)
	curl -s "https://slack.com/api/users.getPresence?token=${token}" | jq -r '.presence'
	exit
        ;;
    *)
        echo "away or here?"
        exit
        ;;
esac

echo "Set me to ${presence} on Slack."
curl -s "https://slack.com/api/users.setPresence?token=${token}&presence=${presence}&pretty=1"
