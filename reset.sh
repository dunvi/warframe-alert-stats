#!/bin/bash

# remove all entries in the database
mongo warframe --eval "db.dropDatabase()"

# clear the saved last_id - this will signal
# to fetchalerts.py that we want to repopulate
# with all historical alerts
rm last_id
touch last_id

# lazy
./update.sh

