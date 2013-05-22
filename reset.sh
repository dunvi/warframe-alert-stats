#!/bin/bash
mongo warframe --eval "db.dropDatabase()"
rm last_id
touch last_id
./update.sh

