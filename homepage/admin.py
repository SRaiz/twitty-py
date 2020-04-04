from django.contrib import admin

from .models import Tweet


class TweetAdmin( admin.ModelAdmin ):
    list_display = ('id', 'created_at', 'text', 'user_name', 'user_screenname', 'location', 'description', 'followers_count', 'friends_count', 'tweet_language', 'gender')

admin.site.register(Tweet, TweetAdmin)
