Warframe Alert Statistics
====================

stats tracking for warframe alerts

currently only updates when I manually run the update script
(the database is on my laptop which is oh-so-useful).

currently generates statistics for:
* calculates distribution of alerts over the day
    * in 30 minute blocks
    * and in 15 minute blocks
* calculates average duration
* calculates distribution of credit awards
    * for all time
    * since update 7.8.0
* calculates the average credit award
    * for all time
    * since update 7.8.0
* calculates percentage of credit awards that are 2000cr
    * for all time
    * since update 7.8.0
* calculates number of each special alert
* calculates frequency of special alerts
* calculates distribution of the start time of potato alerts

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
