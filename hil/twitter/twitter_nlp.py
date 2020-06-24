###################################################################################
# TWITTER NLP
###################################################################################

###################################################################################

import os
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
import operator
import json
from collections import Counter
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
#nltk.download('punkt')
import gensim
from gensim import corpora
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

###################################################################################

# SET UP WORKING DIRECTORY
os.chdir("/Users/a.a.gonzalez.paje/Box Sync/Alberto/rapid_intel/iter_2/tw_listener")
os.getcwd()

# IMPORT DATA AND PRINT HEADERS
df = pd.read_json("listener_results.json", orient = 'records', lines = True)
print(df.shape)
print(df.head(2))
print(df.columns.values)

###################### CLEANING ######################

# REMOVE LINKS AND SPECIAL CHARACTERS
def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# apply the cleaning function above to the column in a dataframe with tweet texts and print head (first 5 rows)
df['text_clean'] = np.array([clean_tweet(tweet) for tweet in df['text']])
print(df['text_clean'].head())

# example
tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(clean_tweet(tweet))

# Try to remove rt
stop_it = stopwords.words('english') + ['rt','RT','via','️','❗','…']

# steming, remove stopwords and to lowercase
def clean_tweet_ngrams(tweet, stemming=False):
    '''
    Utility function to clean the text in a tweet by transforming to lower case,
    stemming and removing stopwords
    '''
    tweet = tweet.lower()
    tweet = tweet.split()
    if stemming == False:
        tweet = [word for word in tweet if not word in stop_it]
    else:
        ps = PorterStemmer()
        tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    return tweet

# apply the cleaning function above to the dataframe column with text to clean and print head (first 5 rows)
# can be applied to text preprocessed with clean_tweet function for further pre-processing
df['text_clean_ngrams'] = np.array([ clean_tweet_ngrams(tweet) for tweet in df['text_clean'] ])
print(df['text_clean_ngrams'].head())

# # Cleaning - alternative cleaning to preserve links, hashtags and @
# emoticons_str = r"""
#     (?:
#         [:=;] # Eyes
#         [oO\-]? # Nose (optional)
#         [D\)\]\(\]/\\OpP] # Mouth
#     )"""
#
# regex_str = [
#     emoticons_str,
#     r'<[^>]+>',  # HTML tags
#     r'(?:@[\w_]+)',  # @-mentions
#     r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
#     r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
#
#     r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
#     r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
#     r'(?:[\w_]+)',  # other words
#     r'(?:\S)'  # anything else
# ]
#
# tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
# emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)
#
#
# def tokenize(s):
#     return tokens_re.findall(s)
#
#
# def preprocess(s, lowercase=False):
#     tokens = tokenize(s)
#     if lowercase:
#         tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
#     return tokens
#
# # Example
# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(preprocess(tweet))

###################### TERM FREQUENCIES ######################

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt','RT','via','️','❗','…']

def counting_terms(term_type='terms_stop', fname='listener_results.json',nwords =5):
    with open(fname, 'r') as f:
        count_all=Counter()
        for line in f:
            tweet=json.loads(line)
            # Create a list with  terms
            if term_type == 'terms_all':
                terms_all = [term for term in preprocess(tweet['text'],True)]
                # Update the counter
                count_all.update(terms_all)
            elif term_type == 'terms_stop':
                terms_stop = [term for term in preprocess(tweet['text'],True) if term not in stop]
                # Update the counter
                count_all.update(terms_stop)
            elif term_type == 'terms_hash':
                terms_hash = [term for term in preprocess(tweet['text'],True)
                  if term.startswith('#')]
                # Update the counter
                count_all.update(terms_hash)
            else:
                terms_only = [term for term in preprocess(tweet['text'],True)
                  if term not in stop and
                  not term.startswith(('#', '@'))]
                count_all.update(terms_only)
        # Print the first 5 most frequent words
        print(count_all.most_common(nwords))
        return count_all


# N MOST COMMON
term_freq=counting_terms(term_type='terms_all', fname='listener_results.json', nwords = 10)

# N MOST COMMON EXCLUDING STOPWORDS, PUNCTUATION AND RT, VIA
term_freq_stop=counting_terms(term_type='terms_stop', fname='listener_results.json',nwords=10)

# N MOST COMMON HASH ONLY
term_freq_hash=counting_terms(term_type='terms_hash', fname='listener_results.json',nwords=10)

# COUNTING JUST TERMS
term_freq_only=counting_terms(term_type='terms_only', fname='listener_results.json',nwords=10)


###################### BIGRAMS ######################

# CREATE BIGRAMS
tokens = df['text_clean_ngrams'].apply(nltk.word_tokenize)
# Flatening nested list
flat_tokens = [term for sublist in tokens for term in sublist]
bgs = nltk.bigrams(flat_tokens)

# FREQUENCY DISTRIBUTION FOR ALL BIGRAMS
fdist = nltk.FreqDist(bgs)
for k,v in fdist.items():
    print(k,v)

fdist_10 = fdist.most_common(10)
print(fdist_10)

# CONVERT TO DF AND SORT
labels = ['bigram', 'Weight']
df_bigrams = pd.DataFrame([tuple_item for tuple_item in fdist.items()], columns =labels)
df_bigrams[['Source_Name','Target_Name']]=pd.DataFrame([tuple_item for tuple_item in df_bigrams.bigram])

# sort in descending order
df_bigrams.sort_values(by='Weight',ascending=False).head(10)

# SUBSET BY WEIGHT
df_bigrams_sub=df_bigrams[df_bigrams['Weight']>5]
print(df_bigrams_sub)

# GENERATE NETWORK FILES FOR GEPHI

# Select multi-level index columns
idx =['bigram','Weight']

# Then pivot the dataset based on this multi-level index
multi_indexed_df = df_bigrams_sub.set_index(idx)
multi_indexed_df.head(2)
multi_indexed_df.columns.name = 'word1_2'

# Stack the columns to achieve the baseline long format for the data
stacked_df = multi_indexed_df.stack(dropna=False)
stacked_df.name = 'Label'
stacked_df.head()

# reset index
stacked_df=stacked_df.reset_index()
print(stacked_df.head())

# TABLE 1 / NODES
# generate list with unique bigrams
print('shape stacked_df:',stacked_df.shape)
Label_unique=stacked_df.Label.unique()
print(Label_unique[0:2])
print('length unique labels:',len(Label_unique))

gephi1 = []
i=0
for item in Label_unique:
    i=i+1
    gephi1.append({'Label': item, 'Id': i})

gephi1=pd.DataFrame(gephi1)
print(gephi1.head())

mydict={}
i = 0
for item in Label_unique:
    i = i+1
    mydict[item] = i

gephi1[['Id','Label']].to_csv('gephi_bigrams_table_nodes.csv',index=False)
print(gephi1.head())

# TABLE 2 / RELATIONS
df_bigrams_sub['Source']=np.array([mydict[item] for item in df_bigrams_sub['Source_Name']])
df_bigrams_sub['Target']=np.array([mydict[item] for item in df_bigrams_sub['Target_Name']])
print(df_bigrams_sub.head(2))

df_bigrams_sub[['Source','Target','Weight']].to_csv('gephi_bigrams_table_relations.csv',index=False)


###################### SENTIMENT ######################

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

df['SA'] = np.array([analize_sentiment(tweet) for tweet in df['text_clean']])
print(df.head(2))

pos_tweets = [tweet for index, tweet in enumerate(df['text']) if df['SA'][index] > 0]
print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(df['text'])))

neu_tweets = [tweet for index, tweet in enumerate(df['text']) if df['SA'][index] == 0]
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(df['text'])))

neg_tweets = [tweet for index, tweet in enumerate(df['text']) if df['SA'][index] < 0]
print("Percentage of negative tweets: {}%".format(len(neg_tweets)*100/len(df['text'])))

neg_tweets_df = df[df['SA']<0]
neu_tweets_df = df[df['SA']==0]
pos_tweets_df = df[df['SA']>0]

df.head()

print(neg_tweets_df['text_clean'].head())

# EXPORT FULL DF TO CSV
df.to_csv('full_df.csv',encoding='utf-8')

###################### TOPIC MODELING ######################

# CREATE CORPUS
dictionary = corpora.Dictionary(tokens)
print(dictionary)

# DOCUMENT TERM MATRIX
doc_term_matrix = [dictionary.doc2bow(tweet) for tweet in tokens]

# LDA MODEL
# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel
# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes=50)


# TIF VECTORIZER
tf_vectorizer = CountVectorizer(min_df = 10)
dtm_tf = tf_vectorizer.fit_transform(df['text_clean_ngrams'])
tf_feature_names = tf_vectorizer.get_feature_names()
print(dtm_tf.shape)


# TIF-IDF VECTORIZER
tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
dtm_tfidf = tfidf_vectorizer.fit_transform(df['text_clean_ngrams'])
print(dtm_tfidf.shape)


# LDA MODELS
lda_tf = LatentDirichletAllocation(n_topics=10, random_state=0)
lda_tf.fit(dtm_tf)

# DISPLAY TOPICS
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))


no_top_words = 10
display_topics(lda_tf, tf_feature_names, no_top_words)


###################################################################################






































































