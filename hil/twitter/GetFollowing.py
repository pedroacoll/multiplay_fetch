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


# GET FRIENDS AND FRIENDS OF FRIENDS
def get_follower_ids(centre, max_depth=1, current_depth=0, taboo_list=[]):

    if current_depth == max_depth:
        print 'out of depth'
        return taboo_list

    if centre in taboo_list:
        # we've been here before
        print 'Already been here.'
        return taboo_list
    else:
        taboo_list.append(centre)

    try:
        userfname = os.path.join(USER_DIR, str(centre) + '.json')
        if not os.path.exists(userfname):
            print 'Retrieving user details for twitter id %s' % str(centre)
            while True:
                try:
                    user = api.get_user(centre)

                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'profile_image_url' : user.profile_image_url,
                         'created_at' : str(user.created_at),
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'followers_ids': user.followers_ids()}

                    with open(userfname, 'w') as outf:
                        outf.write(json.dumps(d, indent=1))

                    user = d
                    break
                except tweepy.TweepError, error:
                    print type(error)

                    if str(error) == 'Not authorized.':
                        print 'Can''t access user data - not authorized.'
                        return taboo_list

                    if str(error) == 'User has been suspended.':
                        print 'User suspended.'
                        return taboo_list

                    errorObj = error[0][0]

                    print errorObj

                    if errorObj['message'] == 'Rate limit exceeded':
                        print 'Rate limited. Sleeping for 15 minutes.'
                        time.sleep(15 * 60 + 15)
                        continue

                    return taboo_list
        else:
            user = json.loads(file(userfname).read())

        screen_name = enc(user['screen_name'])
        fname = os.path.join(FOLLOWING_DIR, screen_name + '.csv')
        friendids = []

        if not os.path.exists(fname):
            print 'No cached data for screen name "%s"' % screen_name
            with open(fname, 'w') as outf:
                params = (enc(user['name']), screen_name)
                print 'Retrieving friends for user "%s" (%s)' % params

                # page over friends
                c = tweepy.Cursor(api.friends, id=user['id']).items()

                friend_count = 0
                while True:
                    try:
                        friend = c.next()
                        friendids.append(friend.id)
                        params = (friend.id, enc(friend.screen_name), enc(friend.name))
                        outf.write('%s\t%s\t%s\n' % params)
                        friend_count += 1
                        if friend_count >= MAX_FRIENDS:
                            print 'Reached max no. of friends for "%s".' % friend.screen_name
                            break
                    except tweepy.TweepError:
                        # hit rate limit, sleep for 15 minutes
                        print 'Rate limited. Sleeping for 15 minutes.'
                        time.sleep(15 * 60 + 15)
                        continue
                    except StopIteration:
                        break
        else:
            friendids = [int(line.strip().split('\t')[0]) for line in file(fname)]

        print 'Found %d friends for %s' % (len(friendids), screen_name)

        # get friends of friends
        cd = current_depth
        if cd+1 < max_depth:
            for fid in friendids[:FRIENDS_OF_FRIENDS_LIMIT]:
                taboo_list = get_follower_ids(fid, max_depth=max_depth,
                    current_depth=cd+1, taboo_list=taboo_list)

        if cd+1 < max_depth and len(friendids) > FRIENDS_OF_FRIENDS_LIMIT:
            print 'Not all friends retrieved for %s.' % screen_name

    except Exception, error:
        print 'Error retrieving followers for user id: ', centre
        print error

        if os.path.exists(fname):
            os.remove(fname)
            print 'Removed file "%s".' % fname

        sys.exit(1)

    return taboo_list

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
    ap.add_argument("-d", "--depth", required=True, type=int, help="How far to follow user network")
    args = vars(ap.parse_args())

    twitter_screenname = args['screen_name']
    depth = int(args['depth'])

    if depth < 1 or depth > 5:
        print 'Depth value %d is not valid. Valid range is 1-5.' % depth
        sys.exit('Invalid depth argument.')

    print 'Max Depth: %d' % depth
    matches = api.lookup_users(screen_names=[twitter_screenname])

    if len(matches) == 1:
        print get_follower_ids(matches[0].id, max_depth=depth)
    else:
        print 'Sorry, could not find twitter user with screen name: %s' % twitter_screenname
















