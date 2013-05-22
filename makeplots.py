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

plt.clf()

print 

# average duration
durations = [alert["duration"] for alert in alertdb.find()]
averageduration = sum(durations)/len(durations)
print "average duration:", averageduration

print

# credit awards
credits = [alert["credits"] for alert in alertdb.find()]
averagecredits = sum(credits)/len(credits)
print "average credits:", averagecredits

print

plt.xticks(rotation = 25)

plt.hist(credits, bins=50)
plt.savefig('creditdist-all')
print "created creditdist-all.png"

plt.clf()

print

credits = [alert["credits"] for alert in alertdb.find()
            if alert["start"] > datetime(year=2013,
                month=4,
                day=19,
                hour=21,
                minute=30)]
averagecredits = sum(credits)/len(credits)
print "average credits since update 7.8.0:", averagecredits

print

plt.xticks(rotation = 25)

plt.hist(credits, bins=50)
plt.savefig('creditdist-7-8-0')
print "created creditdist-7-8-0.png"

plt.clf()

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
    print artifact[0], (18-len(artifact[0]))*" ", ":", artifact[1]

print

current = { }
for blueprint in blueprints:
    if blueprint["blueprint"] in current.keys():
        current[blueprint["blueprint"]] += 1
    else:
        current[blueprint["blueprint"]] = 1

print "Types of blueprints:", blueprints.count()
for blueprint in current.iteritems():
    print blueprint[0], (18-len(blueprint[0]))*" ", ":", blueprint[1]

print

current = { "reactor" : 0, "catalyst" : 0 }
for potato in potatoes:
    current[potato["potato"]] += 1

print "Types of potatoes:", potatoes.count()
print "Orokin Reactor  :", current["reactor"]
print "Orokin Catalyst :", current["catalyst"]

print

