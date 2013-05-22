Warframe Alert Statistics
====================

stats tracking for warframe alerts

currently only updates when I manually run the update script
(the database is on my laptop which is oh-so-useful).

currently generates statistics for:
* distribution of alerts over the day

data taken from the twitter (@WarframeAlerts)

considering trying to make real time tracking as more alerts 
happen, but for now just starting with the basics.

:D

#### want your own?
Sorry, I'm not gonna make it easy, but I will tell you what
I am using.

You will need:
* mongodb (or update all the scripts to your database of choice)
* pymongo
* matplotlib
* python-twitter
* (may use MongoKit later on if I decide I want data validation)
