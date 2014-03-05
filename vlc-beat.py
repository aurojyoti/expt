import os
import ntpath

from twitter import *

import logging

from apscheduler.scheduler import Scheduler

logging.basicConfig()

#twitter credentials
CONSUMER_KEY = 'uLpEOGl4jawU8MnJebsCFg' 
CONSUMER_SECRET = '6075Qb2WqpnxBTBJJrSpvO2h4oLTjbME6GqpQZN2Y' 
ACCESS_TOKEN_KEY = '63371007-gcN9bTiYZ6bN2rnZrRvqOQ6hLgHhMIW4WztDJEEFd' 
ACCESS_TOKEN_SECRET = 'mVe5QJXhvpeqoQkQuaOBFa3Qka2PxWSqTw8F7adrOG1y1'

t = Twitter(
            auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
            )

POSSIBLE_AUDIO_EXTENSIONS = ['mp3', 'wav']
POSSIBLE_VIDEO_EXTENSIONS = ['mp4', 'flv', 'mov', 'mkv', 'avi']
COMMAND="lsof -c vlc | grep REG | grep -v -e '\.[ms]o' -e 'SYSV' -e 'font'"

schedule_job = Scheduler()

def parse_path(path):
        file_path, file_name = ntpath.split(path)
        return file_name or ntpath.basename(file_path)
        
#class Twitter(): 
 #   def __init__(self, access_token_secret = ACCESS_TOKEN_SECRET, access_token_key=ACCESS_TOKEN_KEY,
  #                      consumer_secret=CONSUMER_SECRET, consumer_key=CONSUMER_KEY):
   #     self.api = twitter.Api(access_token_secret = access_token_secret,
    #                               access_token_key=access_token_key,
     #                              consumer_secret=consumer_secret,
      #                             consumer_key=consumer_key)
        
    #def post_tweet(self, tweet_text):
     #   self.api.PostUpdate(tweet_text)
            
            
            
class VLCMonitor():   
    def __init__(self, interval=3):
        self.state = self.get_vlc_state()
        self.error = None
        self.interval = interval
 
 
    def get_current_vlc_status(self):
        terminal_output=os.popen(COMMAND,"r")
        lines = terminal_output.readlines()
        if lines:
            last_line = lines[-1]
            file_path = ' '.join(last_line.split()[8:]).strip()
            
            if file_path.split('.')[-1] in POSSIBLE_AUDIO_EXTENSIONS:
                return {'vlc_running':True, 'type': 'audio', 'path':file_path}
                
            elif file_path.split('.')[-1] in POSSIBLE_VIDEO_EXTENSIONS:
                return {'vlc_running':True, 'type': 'video', 'path':file_path}
                
            else:
                return {'vlc_running':True, 'type': None, 'path':None} 
        else:
            return {'vlc_running':False} 
    
    def get_vlc_state(self):
        vlc_data = self.get_current_vlc_status()
        if vlc_data['vlc_running']:
            if vlc_data['type'] == 'audio':
                return [True, 'Listening to', parse_path(vlc_data['path'])]
            elif vlc_data['type'] == 'video':
                 return [True, 'Watching', parse_path(vlc_data['path'])]
            else:
                 return (True, 'Nothing Being Played on VLC', '')
        else:
            return [False, 'VLC Not Running', '']
    


vlc_monitor = VLCMonitor()
#twitter_client = Twitter()

@schedule_job.interval_schedule(seconds=3)
def job():
    try:
        vlc_monitor.error = None
        new_state = vlc_monitor.get_vlc_state()
        if new_state != vlc_monitor.state:
            vlc_monitor.state = new_state
            status = ' '.join(vlc_monitor.state[1:])
            print status
            
            if vlc_monitor.state[0] and vlc_monitor.state[2]:
                #this is where you can change the text to be tweeted 
                #to_tweet = status + '   VLC Media Player - via VLCBeat'
                t.statuses.update(to_tweet = status + '   VLC Media Player - via VLCBeat')
                
    except KeyboardInterrupt:
        print 'VLC monitor exiting...'
    except Exception, e:
        vlc_monitor.error = str(e)
        print 'An Error Occured.. \n', vlc_monitor.error
      

  
def run():
    print 'VLC Monitor starting...'
    vlc_monitor.state = vlc_monitor.get_vlc_state()
    print ' '.join(vlc_monitor.state[1:])
    schedule_job.start()
    while True:
        try:
             pass
        except KeyboardInterrupt:
             print 'VLC monitor exiting...'


run()