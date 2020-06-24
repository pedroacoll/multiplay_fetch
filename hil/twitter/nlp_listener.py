# ANALYSING LISTENER DATA
# https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-

# IMPORT MODULES
import os
import pandas as pd
import numpy as np
from textblob import TextBlob
import regex
import operator
import json
from collections import Counter



# SET UP WORKING DIRECTORY
path = "/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/iter_2/tw_listener"
os.chdir("/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/iter_2/tw_listener")
os.getcwd()


# GET THE JSON FILE
df = pd.read_json("listener_results.json", orient = 'records', lines = True)
df.shape
print df.head(10)
print df.columns.values


# CLEAN RESULTS
def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(regex.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# SENTIMENT ANALYSIS
def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

# ADD SENTIMENT RESULT
df['SA'] = np.array([ analize_sentiment(tweet) for tweet in df['text'] ])
print df.head(10)

pos_tweets = [ tweet for index, tweet in enumerate(df['text']) if df['SA'][index] > 0]
print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(df['text'])))

neu_tweets = [ tweet for index, tweet in enumerate(df['text']) if df['SA'][index] == 0]
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(df['text'])))

neg_tweets = [ tweet for index, tweet in enumerate(df['text']) if df['SA'][index] < 0]
print("Percentage of negative tweets: {}%".format(len(neg_tweets)*100/len(df['text'])))


# COUNTING TERMS
fname = 'listener_results.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_all = [term for term in tweet['text']]
        # Update the counter
        count_all.update(terms_all)
    # Print the first 5 most frequent words
    print(count_all.most_common(5))


































