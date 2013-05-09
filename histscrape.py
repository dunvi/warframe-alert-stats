#!usr/bin/python
#
# works! :D

import twitter
api = twitter.Api()

counter = 0
for i in xrange(1,8):
    alerts = api.GetUserTimeline(1344755923, count=200, page=i)

    for alert in alerts:
        print counter, alert.created_at, alert.text
        counter += 1

