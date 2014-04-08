Cloud-Proj2 : TwittMap
===========

Instructions
Assignment 2: TwittMap

Due Date: 4/17/14

You need to create a Google App Engine based TwittMap. The closest example I had shown in the class is: http://worldmap.harvard.edu/tweetmap/

For the base version, you need the following:

Collect about 100MB twits using Twitter API from GAE application
Parse the Twits and store in Datastore. The parsed twits should have location information and a set of key words from the content of the twits.
You create a scatter plot or any nice plot that depicts all the twits with a the density map - perhaps with color gradient etc.
You should provide a filter that allows a drop down keywords to choose from and only shows twits with those keywords on a google map.
memcache should be used for already seen queries.
Advanced Version: +25

create a timeline - meaning with progression of days, twit map should be rendered.
nicer heat map
every midnight, you get new twits and replot. use scheduled task service.
Extra Advanced: +25

mobile interface
shows timeline in an innovative way to see the twit trends
dynamic keyword dictionary from the analysis of twit contents
