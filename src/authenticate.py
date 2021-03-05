import tweepy
import logging
import os
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger()
load_dotenv(find_dotenv())

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

token = os.getenv("BEARER")

if __name__ == "__main__":
    ### See PIN-based authorization for details at
    ### https://dev.twitter.com/docs/auth/pin-based-authorization

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback='oob')

    # get access token from the user and redirect to auth URL
    auth_url = auth.get_authorization_url()
    print ('Authorization URL: ' + auth_url)

    # ask user to verify the PIN generated in broswer
    verifier = input('PIN: ').strip()
    auth.get_access_token(verifier)
    print ('ACCESS_KEY = "%s"' % auth.access_token)
    print ('ACCESS_SECRET = "%s"' % auth.access_token_secret)