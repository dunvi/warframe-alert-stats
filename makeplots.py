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

# the times
starttimes = [d.date2num(datetime.combine(date.today(),
                                          alert["start"].time()))
                for alert in alertdb.find()]

xfmt = d.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(xfmt)
plt.xticks(rotation = 25)

plt.hist(starttimes, bins=48)
plt.savefig('timedist-30')

plt.clf()

plt.hist(starttimes, bins=96)
plt.savefig('timedist-15')

