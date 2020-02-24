import os

import tweepy
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'pageheader': 'Dashboard'})


def authenticate_twitter(request):
    #   Get all the environment variables
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')

    #   Call the OAuth2 authentication using tweepy
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    #   The search term and date from which data is required. Retweets are filtered here
    search_words = '#bushfires' + ' -filter:retweets'
    date_since = '2020-02-01'

    #   Collect Tweets
    tweets = tweepy.Cursor( api.search, q = search_words, lang = 'en', since = date_since, tweet_mode = 'extended' ).items(5)

    tweets_to_show = []
    for tweet in tweets:
        # print('================')
        # print(tweet.entities.unwound.url)
        # print('================')
        temp_tweet = {
            'created_at': tweet.created_at,
            'id': tweet.id,
            'text': tweet.full_text,
            'user': {
                'name': tweet.user.name,
                'screen_name': tweet.user.screen_name,
                'location': tweet.user.location,
                'description': tweet.user.description
            }
            #'url': tweet.entities.urls
        }
        tweets_to_show.append(temp_tweet)


    return render(request, 'home.html', {'tweets': tweets_to_show})
