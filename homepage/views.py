import json
import os

import tweepy
from django.http import HttpResponse
from django.shortcuts import render
from genderize import Genderize

import update_sql

from .models import Tweet


def home(request):
    tweets = Tweet.objects.all();
    return render(request, 'home.html', {'pageheader': 'Dashboard', 'tweets': tweets})


def authenticate_twitter(request):
    #   Get all the environment variables
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')

    #   Call the OAuth2 authentication using tweepy
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    #   The search term and date from which data is required. Retweets are filtered here
    search_words = '#LearnFromHome' + ' -filter:retweets'
    date_since = '2020-03-01'

    #   Collect Tweets
    tweets = tweepy.Cursor( api.search, q = search_words, lang = 'en', since = date_since, tweet_mode = 'extended' ).items()

    tweets_to_show = []
    counter = 1
    for tweet in tweets:
        print('====')
        json_str = json.dumps(tweet._json)
        
        tweets_to_show.append(
            {
                'created_at': tweet.created_at,
                'id': tweet.id,
                'text': tweet.full_text,
                'user_name': tweet.user.name,
                'user_screenname': tweet.user.screen_name,
                'location': tweet.user.location,
                'description': tweet.user.description,
                'followers_count': tweet.user.followers_count,
                'friends_count': tweet.user.friends_count,
                'tweet_language': tweet.lang,
                'gender': get_gender(tweet.user.name.split(' ')[0])
            }
        )

    tweets_df = update_sql.update_tweets(tweets_to_show)
    
    tweets = Tweet.objects.all()
    return render(request, 'home.html', {'tweets': tweets})


def get_gender(name):
    name_det = Genderize().get([name])
    return name_det[0].get('gender')
