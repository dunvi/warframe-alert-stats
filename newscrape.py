#!usr/bin/python
#

from datetime import datetime
import twitter

import credentials
api = twitter.Api(consumer_key = credentials.consumer_key(),
                  consumer_secret = credentials.consumer_secret(),
                  access_token_key = credentials.access_token_key(),
                  access_token_secret = credentials.access_token_secret())

if ( api.VerifyCredentials() == None):
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
    
# will not be in date order, but who cares?
        for alert in alerts:
            # get last_id if it's the very first one
            if last_id == '':
                f = open('last_id', 'w')
                f.write(str(alert.id))
                f.close()
                last_id = alert.id

            current_max_id = alert.id - 1
            print alert.created_at, alert.text

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
        print alert.created_at, alert.text

