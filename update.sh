#!/bin/bash
rm stats.txt
touch stats.txt
python newscrape.py
python makeplots.py >> stats.txt

