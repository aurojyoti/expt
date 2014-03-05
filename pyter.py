import sys
from twitter import *

tweet = " "
len = len(sys.argv)
sys.argv = sys.argv[1:len]
for word in sys.argv:
	tweet += " "+word

CONSUMER_KEY = '' 
CONSUMER_SECRET = '' 
ACCESS_TOKEN_KEY = '' 
ACCESS_TOKEN_SECRET = ''

t = Twitter(
            auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
            )

t.statuses.update(status = "Py says -"+ tweet)
print "TWEETED Py says -", tweet

