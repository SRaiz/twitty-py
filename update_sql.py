import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def update_tweets( tweets ):
    
    engine = create_engine('postgresql+psycopg2://postgres:tweety_336600@localhost:5432/tweety-py')

    #   Store tweets in dataframe and send it to the database
    tweets_df = pd.DataFrame(tweets)
    tweets_df.to_sql('homepage_tweet', engine, if_exists='replace')
