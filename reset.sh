#!/bin/bash
mongo warframe --eval "db.dropDatabase()"
rm last_id
touch last_id
python newscrape.py
python makeplots.py

