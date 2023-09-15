#!/bin/bash

display_notification () {
    osascript -e 'display notification "Failed" with title "amazon_ranking.py"'
}

DATE=$(date +"%Y%m%d_%H%M")
LOGFILE="../log/AR$DATE.log"
cd /Users/otchy/Documents/GitHub/Python/Amazon_Ranking/
../.venv/bin/python amazon_ranking.py 1>$LOGFILE 2>&1
PY_STATUS=$?
if [ $PY_STATUS -ne 0 ]; then
  display_notification
fi
