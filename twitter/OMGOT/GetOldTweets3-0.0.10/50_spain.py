#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import GetOldTweets3 as got
from datetime import timedelta, date

user = '50trends_es'

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        since= start_date + timedelta(n)
        until=start_date + timedelta(n+1)
        yield(since,until)

start_date = date(2020, 6, 23)
end_date = date(2020, 6, 24)
for since, until in daterange(start_date, end_date):
    since=since.strftime("%Y-%m-%d")
    until=until.strftime("%Y-%m-%d")
    
    archivo='50trends_es/'+since+'.csv'
    print(archivo)

    tweetCriteria = got.manager.TweetCriteria().setUsername(user)\
                                               .setSince(since)\
                                               .setUntil(until)
    outputFile = open(archivo, "w+", encoding="utf8")
    outputFile.write('date,username,to,replies,retweets,favorites,text,geo,mentions,hashtags,id,permalink\n')                                           
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for t in tweets:
        data = [t.date.strftime("%Y-%m-%d %H:%M:%S"),
                t.username,t.to or '',
                t.replies,
                t.retweets,
                t.favorites,
                '"'+t.text.replace('"','""')+'"',
                t.geo,t.mentions,t.hashtags,
                t.id,t.permalink]
        data[:] = [i if isinstance(i, str) else str(i) for i in data]
        outputFile.write(','.join(data) + '\n')
    outputFile.flush()
    outputFile.close()
