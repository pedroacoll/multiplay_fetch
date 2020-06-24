# LISTEN TO TW STREAMING API

# IMPORT MODULES
import os
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


# SET UP WORKING DIRECTORY
path = "/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/iter_2/tw_listener"
os.chdir("/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/iter_2/tw_listener")
os.getcwd()

# GET CREDENTIALS

# Set up keys (just once)
consumer_key = "R7j6gTZACckvv6M7ktFQUIocr"
consumer_secret = "RJITj1CbWH5uaLBGvZ1Q23rA2ulnIe1B82jMXYSyyIp8Ho4frm"
access_token = "103299888-oZP8BhjgMFasfqKLSYjcI3e66TpDYVX0QUoh7Fiw"
access_secret = "iVw4skwuxnbyP7UWa7k1jYTyyWMgEBrPvUtfe6xVei7Ad"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# STREAMING LISTENER
class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('listener_results.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#feel'])


# Run to see current results: wc -l listener_results.json









