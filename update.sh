#!/bin/bash
rm stats.txt
touch stats.txt
python newscrape.py >> stats.txt
python makeplots.py >> stats.txt

