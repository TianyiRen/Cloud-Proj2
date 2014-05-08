import time
from datetime import datetime, timedelta

def strtodatetime(timestr):
	# example: '2014-04-12 01:26:23'
	t = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
	dt = datetime.fromtimestamp(time.mktime(t))
	return dt