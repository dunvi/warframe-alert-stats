#!usr/bin/python
#

import time
from datetime import datetime

def make_document(alert):
    timestamp = time.strptime(alert.created_at, "%a %b %d %H:%M:%S +0000 %Y")
       
    text = alert.text.split()
    info = " ".join(text[2:]).split(" - ")
            
    duration = info[1]
    if duration[-1] == 'm':
        duration = int(duration[:-1])
    elif duration[-1] == 'h':
        duration = 60*int(duration[:-1])
    else:
        duration = None
        print "could not parse duration"

    current = {"_id" : alert.id,
             "start" : datetime.fromtimestamp(time.mktime(timestamp)),
            "planet" : text[2][1:-2],
           "mission" : text[1],
       "description" : info[0],
          "duration" : duration,
           "credits" : int(info[2][:-2]),
    }

    if len(info) > 3:
        lookat = info[3]
        if "Artifact" in lookat:
            current["artifact"] = " ".join(lookat.split()[:-1])
        elif "Orokin Reactor" in lookat:
            current["potato"] = "reactor"
        elif "Orokin Catalyst" in lookat:
            current["potato"] = "catalyst"
        elif "Blueprint" in lookat:
            current["blueprint"] = " ".join(lookat.split()[:-1])
 
    if len(info) > 4:
        print "more arguments than expected!"

    return current

import twitter
from pymongo import MongoClient
db = MongoClient().warframe
alertdb = db.alerts

import credentials
api = twitter.Api(consumer_key = credentials.consumer_key(),
                  consumer_secret = credentials.consumer_secret(),
                  access_token_key = credentials.access_token_key(),
                  access_token_secret = credentials.access_token_secret())

if (api.VerifyCredentials() == None):
    sys.exit("Error with credentials!")

warframe = 1344755923

f = open('last_id')
last_id = f.read()
f.close()

if last_id == '':
    current_max_id = None
    while True:
        alerts = api.GetUserTimeline(user_id = warframe,
                                     count = 200,
                                     max_id = current_max_id)

        if alerts == []:
            break
    
        for alert in alerts:
            # get last_id if it's the very first one
            if last_id == '':
                f = open('last_id', 'w')
                f.write(str(alert.id))
                f.close()
                last_id = alert.id

            current_max_id = alert.id - 1
            current = make_document(alert)
            alertdb.insert(current)

# now we have all historical alerts. 

first = True
current_max_id = None
while True:
# are you kidding me? use since_id T.T
    alerts = api.GetUserTimeline(user_id = warframe,
                                 since_id = last_id,
                                 count = 200,
                                 max_id = current_max_id)
    
    if alerts == []:
        break

# save the id of the most recent tweet accessed
    for alert in alerts:
        if first:
            f = open('last_id', 'w')
            f.write(str(alert.id))
            f.close()
            first = False
        
        current_max_id = alert.id - 1
        current = make_document(alert)
        alertdb.insert(current)

# some sanity checks
print "number of tweets found: ", alertdb.count()

