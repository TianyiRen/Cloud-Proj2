Cloud-Proj2 : TwittMap
===========

Instructions
Assignment 2: TwittMap
url: twittmap-xhcyfz.appspot.com
Due Date: 4/17/14


You need to create a Google App Engine based TwittMap. The closest example I had shown in the class is: http://worldmap.harvard.edu/tweetmap/

For the base version, you need the following:

	1. Collect about 100MB twits using Twitter API from GAE application
	2. Parse the Twits and store in Datastore. The parsed twits should have location information and a set of key words from the content of the twits.
	3. You create a scatter plot or any nice plot that depicts all the twits with a the density map - perhaps with color gradient etc.
	4. You should provide a filter that allows a drop down keywords to choose from and only shows twits with those keywords on a google map.
	5. memcache should be used for already seen queries.

Advanced Version: +25

	1. create a timeline - meaning with progression of days, twit map should be rendered.
	2. nicer heat map
	3. every midnight, you get new twits and replot. use scheduled task service.

Extra Advanced: +25

	1. mobile interface
	2. shows timeline in an innovative way to see the twit trends
	3. dynamic keyword dictionary from the analysis of twit contents

===============================
development reference

Twitter API links:
For collecting tweets without query: GET statuses/sample
https://dev.twitter.com/docs/api/1.1/get/statuses/sample

For collecting tweets with given query: GET search/tweets
https://dev.twitter.com/docs/api/1.1/get/search/tweets

Twitter Python API:
https://github.com/sixohsix/twitter

GAE Application info:
Application ID:	twittmap-xhcyfz

access port: 9080

===============================
useful command

login to EC2
ssh -i zyf.pem ec2-user@54.85.51.169

Run a backgroud process[change log.out & log.err]:

nohup python twitterdata.py > log.out 2> log.err < /dev/null &

copy file to EC2:

scp -i zyf.pem twitterdata.py ec2-user@54.85.51.169:/home/ec2-user/

CloudBox library: jqcloud

http://primegap.net/2011/03/04/jqcloud-a-jquery-plugin-to-build-neat-word-clouds/


ScrollBar library:

http://baijs.com/tinyscrollbar/

LineChart library:

http://www.oesmith.co.uk/morris.js/
