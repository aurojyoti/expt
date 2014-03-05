import sys
from twitter import *

tweet = " "
len = len(sys.argv)
sys.argv = sys.argv[1:len]
for word in sys.argv:
	tweet += " "+word

CONSUMER_KEY = 'uLpEOGl4jawU8MnJebsCFg' 
CONSUMER_SECRET = '6075Qb2WqpnxBTBJJrSpvO2h4oLTjbME6GqpQZN2Y' 
ACCESS_TOKEN_KEY = '63371007-gcN9bTiYZ6bN2rnZrRvqOQ6hLgHhMIW4WztDJEEFd' 
ACCESS_TOKEN_SECRET = 'mVe5QJXhvpeqoQkQuaOBFa3Qka2PxWSqTw8F7adrOG1y1'

t = Twitter(
            auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
            )

t.statuses.update(status = "Py says -"+ tweet)
print "TWEETED Py says -", tweet

