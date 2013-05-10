#!usr/bin/python
#
# works! :D

import twitter
api = twitter.Api()

import matplotlib


counter = 0
i = 1
dataset = {}
while True:
    alerts = api.GetUserTimeline(1344755923, count=200, page=i)

    if alerts == []:
        break

    for alert in alerts:
        data = {}
        info = alert.text
        info = info.split(" ")
        data["mission"] = info[0]
        data["planet"] = info[1][1:-2]
        info = " ".join(info)
        info = info.split(" - ")
        duration = info[1]
        if duration[-1] == "h":
            duration = int(duration[:-1]) * 60
        else:
            duration = int(duration[:-1])
        data["duration"] = duration
        data["credits"] = info[2][:-2]
        if len(info) == 4:
            data["?"] = info[-1]
        dataset[alert.created_at] = data

    i += 1

# at this point, all of the data has been gathered :D

# sort by planet
planetsort = {}
for key in dataset.keys():
    data = dataset[key]
    if data["planet"] not in planetsort.keys():
        planetsort[data["planet"]] = {}
    planetsort[data["planet"]][key] = data
# next sort by mission in planet

