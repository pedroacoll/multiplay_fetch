# GET FRIENDS AND FOLLOWERS

# MODULES
import os
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
import sys
import json
import argparse
from datetime import datetime

# EXECUTION: python GetFollowing.py -s username -d 2

# SET UP WORKING DIRECTORY
path = "/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/iter_2/tw_listener"
os.chdir("/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/iter_2/tw_listener")
os.getcwd()

# CREATE NEW DIRECTORIES
FOLLOWING_DIR = 'following'
USER_DIR = 'twitter-users'
MAX_FRIENDS = 200
FRIENDS_OF_FRIENDS_LIMIT = 200

if not os.path.exists(FOLLOWING_DIR):
    os.makedirs(FOLLOWING_DIR)

if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

enc = lambda x: x.encode('ascii', errors='ignore')


# GET CREDENTIALS

# Set up keys (just once)
consumer_key = "R7j6gTZACckvv6M7ktFQUIocr"
consumer_secret = "RJITj1CbWH5uaLBGvZ1Q23rA2ulnIe1B82jMXYSyyIp8Ho4frm"
access_token = "103299888-oZP8BhjgMFasfqKLSYjcI3e66TpDYVX0QUoh7Fiw"
access_secret = "iVw4skwuxnbyP7UWa7k1jYTyyWMgEBrPvUtfe6xVei7Ad"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def get_followers(user_id):
    users = []
    page_count = 0
    for i, user in enumerate(tweepy.Cursor(api.followers, id=user_id, count=200).pages()):
        print ('Getting page {} for followers'.format(i))
        users += user
    return users


followers = get_followers("StateFarm")


def get_followers_ids(user_id):
    ids = []
    page_count = 0
    for page in tweepy.Cursor(api.followers_ids, id=user_id, count=5000).pages():
        page_count += 1
        print ('Getting page {} for followers ids'.format(page_count))
        ids.extend(page)

    return ids

friends = get_followers_ids("StateFarm")












