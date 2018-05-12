#!/bin/bash

########################################################################################################################################
# @author - Kiran M                                                                                                                    #
########################################################################################################################################

./summariseMessageCount.sh > ./msgCountOut.log

# Send a Notification on Slack Webhook

curl -X POST --data-urlencode "payload={\"channel\": \"#test\", \"username\": \"message-bot\", \"text\": \"*Cleanup Job Dry Run at: `date +"%T"`*`echo -e "\n" && cat ./msgCountOut.log`\", \"icon_emoji\": \":INSERT_EMOJI_REF:\"}" https://hooks.slack.com/services/INSERT_SLACK_TOKEN
