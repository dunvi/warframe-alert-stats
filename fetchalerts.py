#!usr/bin/python
# fetchalerts.py
#   gets alerts
#   establishes a connection to the database
#   parses the alerts and insert them
#
# NOTES:
#   need to check the inconsistency with last_id, but it looks
#       like the python-twitter interface automatically parses
#       the ids into numbers, which means that in places I may
#       have been using strings for the document's _id field.
#       That was silly.
#   trying to use the with idiom for opening and closing files,
#       need to double check that I'm doing it right though :\

# used in the documents
import time
from datetime import datetime

# import the API
import twitter

# import and establish the database connection
from pymongo import MongoClient
db = MongoClient().warframe
alertdb = db.alerts

# set our credentials
# these are established in the credentials.py file which is
# separate so I can keep them secure by just sticking the file
# in the .gitignore file :P
import credentials
api = twitter.Api(consumer_key = credentials.consumer_key(),
                  consumer_secret = credentials.consumer_secret(),
                  access_token_key = credentials.access_token_key(),
                  access_token_secret = credentials.access_token_secret())

# check credentials!
if (api.VerifyCredentials() == None):
    sys.exit("Error with credentials!")

print "Connection made!"

# warframe alert's twitter userid
warframe = 1344755923

###################
#### FUNCTIONS ####
###################

def make_document(alert):
    ''' creates a document for insertion into the database
        input: alert
            this should be the entire tweet as returned
            from the python-twitter interface
        output: mongodb document
            a document ready to be inserted into the database
        expected format of a tweet's text:
<mission> (<planet>): <description> - <duration>[mh] - <credits>cr [- <? award>]
    '''
    # fix the timestamp; twitter API uses a bullshit date order
    timestamp = time.strptime(alert.created_at, "%a %b %d %H:%M:%S +0000 %Y")
       
    # preparsing
    text = alert.text.split()
    info = " ".join(text[2:]).split(" - ")
            
    # ID
    #   use the tweet's id for the db id number
    alertid = alert.id

    # START
    start = datetime.fromtimestamp(time.mktime(timestamp))

    # PLANET
    #    removes the colon and parentheses
    planet = text[1][1:-2]

    # MISSION
    mission = text[0]
    
    # DESCRIPTION
    description = info[0]
    
    # DURATION
    #   convert to minutes
    #   leave in integer form instead of using a timedelta
    #   easier for analysis
    duration = info[1]
    if duration[-1] == 'm':
        duration = int(duration[:-1])
    elif duration[-1] == 'h':
        duration = 60*int(duration[:-1])
    else:
        duration = None
        print "could not parse duration"

    # CREDITS
    credits = int(info[2][:-2])

    current = {"_id" : alertid,
             "start" : start,
            "planet" : planet,
           "mission" : mission,
       "description" : description,
          "duration" : duration,
           "credits" : credits,
    }

    # ? REWARDS
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
 
    # if the tweet was incorrectly formatted, or unparseable
    if len(info) > 4:
        print "more arguments than expected!"

    return current

# retrieve the last_id which is in the plaintext file called as such
#   consider using an evironment variable (pass in to the command line?)
#   once I have a more stable server setup?
# if there has been not read (or you wish to repopulate the database),
#   last_id will be set to an empty string. Otherwise parse to int.
# otherwise, the last_id is the id of the mot recent tweet retrieved,
#   for the next time we initialize the API calls

# safe file opening and closing
with open('last_id') as f:
    last_id = f.read()

# if the database needs to be populated with historical entries
if last_id == '':
    print "Populating database"

    # current_max_id is the oldest tweet that has been retrieved yet
    # handles the paging for us, see the twitter API documentation
    current_max_id = None

    while True:
        # API call
        # retrieves 200 tweets at a time - maximum is 3200
        # returns an empty set if there are no more tweets to retrieve
        alerts = api.GetUserTimeline(user_id = warframe,
                                     count = 200,
                                     max_id = current_max_id)

        if alerts == []:
            break
    
        # run through all alerts...
        for alert in alerts:

            # set the last_id if it's the very first tweet retrieved
            if last_id == '':
                with open('last_id', 'w') as f:
                    f.write(str(alert.id))
                
                last_id = alert.id
            
            # max_id is inclusive
            current_max_id = alert.id - 1
            current = make_document(alert)
            
            # insert the alert into the database!
            alertdb.insert(current)

else: 
    last_id = int(last_id)

# now we have all historical alerts. 

print "Fetching new alerts..."

# gather recent updates from the twitter feed
# first time through, we need to save the since id
first = True
current_max_id = None
while True:

    alerts = api.GetUserTimeline(user_id = warframe,
                                 since_id = last_id,
                                 count = 200,
                                 max_id = current_max_id)
    
    if alerts == []:
        break

    for alert in alerts:
        
        # save the id of the most recent tweet for next time
        if first:
            print "New alerts found!"
            first = False

            with open('last_id', 'w') as f:
                f.write(str(alert.id))
       
        current_max_id = alert.id - 1

        current = make_document(alert)
        
        alertdb.insert(current)

print "Done populating database!"

