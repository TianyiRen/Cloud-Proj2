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
Development Reference

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
Rrequently Used Command

login to EC2:

ssh -i zyf.pem ec2-user@54.85.51.169

Run a backgroud process[change log.out & log.err]:

nohup python twitterdata.py > log.out 2> log.err < /dev/null &

copy file to EC2:

scp -i zyf.pem twitterdata.py ec2-user@54.85.51.169:/home/ec2-user/

=====================================
Front-End libraries

CloudBox library: jqcloud

http://primegap.net/2011/03/04/jqcloud-a-jquery-plugin-to-build-neat-word-clouds/

ScrollBar library:

http://baijs.com/tinyscrollbar/

LineChart library:

http://www.oesmith.co.uk/morris.js/

=====================================
# Readme for TA

GAE url: http://twittmap-xhcyfz.appspot.com/
Team members: Yufei Zhao(yz2605), Xiaohu Chen(xc2263)

Dear TAs,
We have implemented all the functionalities, including advanced and extra advanced. The word cloud on the upper left shows the hottest 50 words in a day. By default, the google map on the right shows geolocation of the latest 10,000 tweets from all over the world while the tweet contents are shown on the lower left. The lower right is a line chart that shown the created time distribution of those 10,000 tweets. This information is updated once a hour.

If you click a word on the word cloud or search a keyword in the search box, the google map, tweets area and line chart are all refreshed to reflect information of that word. For example, the google map will now show the geolocations of the tweets that contain this particular word.

All the searched contents are memcached including hotwords, geolocations etc.

The website is also mobile friedly, as seen in the attached sceenshot. 

Behind the scene, an EC2 server is constantly collecting and parsing tweets using twitter streaming API. A scheduled task in GAE will communicate with the EC2 server once in a hour to get the latest tweets and store into datastore. At the meantime, the related information in memcache (if still valid), for example, the latest 10,0000 tweets geolocations, will be updated so that the no further database query is needed to get the latest information.


