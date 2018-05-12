import os
from datetime import datetime
from slackclient import SlackClient

import time

########################################################################################################################################
# @author - Kiran M                                                                                                                    #
########################################################################################################################################

# Retrieve slack token from Env variable
slack_token = os.environ["SLACK_API_TOKEN"]

# Time period of interest
date_from = "2018-02-10"
date_to = "2018-02-14"

# Channel to work on
channel_id = "C8KA7390D"

# Message content to look for
p1APIMsg = "Message pattern 1"
nonP1APIMsg = "Message pattern 2"

oldest = (datetime.strptime(date_from, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()
latest = (datetime.strptime(date_to, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()

sc = SlackClient(slack_token)

history = sc.api_call("channels.history", count=1000, channel=channel_id, oldest=oldest, latest=latest)

def genericDictIterator(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                genericDictIterator(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                genericDictIterator(v)
            else:
                print v
    else:
        print obj

#genericDictIterator(history)

def clearAndConsolidate(msgLst,msg):
    msgLstLen = len(msgLst)
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(msgLst[0])))
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(msgLst[msgLstLen-1])))
    if msgLstLen > 2:
       print ("Will delete %s %s messages between %s to %s" %(msgLstLen, msg, startTime, endTime))
       for epochTime in msgLst: 
           print ("Deleting message %s" %(epochTime))
           sc.api_call("chat.delete", channel=channel_id, ts=epochTime)

message_by_user = dict([("P1 User", 0),("Non P1 User", 0)])
p1ApiMsgs = []
nonP1ApiMsgs = []
p1PrevMsg = False
nonP1PrevMsg = False

for message in history['messages']:
    # print message['text']
    if message['text'].find(p1APIMsg) != -1:
        p1ApiMsgs.append(message['ts'])
        p1PrevMsg = True
        message_by_user["P1 User"] += 1
    else:
        #print len(p1ApiMsgs)
        if p1PrevMsg == True:
	   clearAndConsolidate(p1ApiMsgs,"P1 API")
           del p1ApiMsgs[:]
        p1PrevMsg = False
    
    if message['text'].find(nonP1APIMsg) != -1:
        nonP1ApiMsgs.append(message['ts'])
        nonP1PrevMsg = True
        message_by_user["Non P1 User"] += 1
    else:
        # print "Second"
        if nonP1PrevMsg == True:
           clearAndConsolidate(nonP1ApiMsgsi,"NonP1 API")
           del nonP1ApiMsgs[:]
        nonP1PrevMsg = False

# For scenarios where the message list does not have breakpoints..
if len(p1ApiMsgs) > 2:
    clearAndConsolidate(p1ApiMsgs,"P1 API")
if len(nonP1ApiMsgs) > 2:
    clearAndConsolidate(nonP1ApiMsgs,"NonP1 API")

for user, count in message_by_user.items():
    print user, 'posted', count, 'messages'
