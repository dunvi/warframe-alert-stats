#!/bin/bash

#FIXME: make fetchalerts return an exit status so
# that we don't remake all of the plots and recalculate
# all of the stats if nothing has changed

#FIXME: make fetchalerts take in the last_id value as
# a command line parameter instead of parsing it 
# through the script itself

#FIXME: after doing the above, make this script take in
# a command line parameter to force makeplots.py to
# run even if there are no database updates 

# since we append to stats.txt instead of rewriting,
# we need to completely remove the old file
rm stats.txt
touch stats.txt

python fetchalerts.py
python makeplots.py >> stats.txt

