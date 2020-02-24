import csv
import sqlite3

import pandas as pd


def update_tweets( tweets ):
    
    db_filename = 'db.sqlite3'
    conn = sqlite3.connect( db_filename )

    #   Store tweets in dataframe and send it to the database
    tweets_df = pd.DataFrame(tweets)
    tweets_df.to_sql('homepage_tweet', conn, if_exists='replace')
