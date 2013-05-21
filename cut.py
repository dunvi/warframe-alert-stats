#!usr/bin/python
#

oldresults = open('results.txt', 'r')
newresults = open('data.txt', 'w')

for line in oldresults:
    newresults.write(" ".join(line.split()[1:])+"\n")

oldresults.close()
newresults.close()
