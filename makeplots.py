#!usr/bin/python
#

from pymongo import MongoClient
db = MongoClient().warframe
alertdb = db.alerts

import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as d
import itertools

from datetime import date, datetime

print

# start time distribution
starttimes = [d.date2num(datetime.combine(date.today(),
                                          alert["start"].time()))
                for alert in alertdb.find()]

# start time distribution - 30 minute bins
xfmt = d.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(xfmt)
plt.xticks(rotation = 25)

plt.hist(starttimes, bins=48)
plt.savefig('timedist-30')
print "created timedist-30.png"

plt.clf()

# start time distribution - 15 minute bins
xfmt = d.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(xfmt)
plt.xticks(rotation = 25)

plt.hist(starttimes, bins=96)
plt.savefig('timedist-15')
print "created timedist-15.png"

print 

# average duration
durations = [alert["duration"] for alert in alertdb.find()]
averageduration = sum(durations)/len(durations)
print "average duration: ", averageduration

print

# frequency of special awards
alertcount = alertdb.count()
artifacts = alertdb.find({ "artifact" : { "$exists" : True } })
blueprints = alertdb.find({ "blueprint" : { "$exists" : True } })
potatoes = alertdb.find({ "potato" : { "$exists" : True } })

afreq = float(artifacts.count())/alertcount
bfreq = float(blueprints.count())/alertcount
pfreq = float(potatoes.count())/alertcount

print "a/b/p frequencies: ", afreq, bfreq, pfreq

print

current = { }
for artifact in artifacts:
    if artifact["artifact"] in current.keys():
        current[artifact["artifact"]] += 1
    else:
        current[artifact["artifact"]] = 1

print "Types of artifacts:", artifacts.count()
for artifact in current.iteritems():
    print artifact[0], (18-len(artifact[0]))*" ", ": ", artifact[1]

current = { }
for blueprint in blueprints:
    if blueprint["blueprint"] in current.keys():
        current[blueprint["blueprint"]] += 1
    else:
        current[blueprint["blueprint"]] = 1

print

print "Types of blueprints:", blueprints.count()
for blueprint in current.iteritems():
    print blueprint[0], (18-len(blueprint[0]))*" ", ": ", blueprint[1]

print
