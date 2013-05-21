#!/bin/bash
rm data.txt
rm last_id
touch last_id
python newscrape.py >> data.txt

