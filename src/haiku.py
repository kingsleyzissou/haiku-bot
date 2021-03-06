import logging
import numpy as np
from tweepy import Cursor, Stream, StreamListener
from twitter import create_api
from pre_processing import pre_process
from post_processing import post_process
from haiku_detection import extract_haiku

logger = logging.getLogger()

# def get_tweet_text(api, id):
#   api.get


def get_tweets(api, query):
    return Cursor(
        api.search,
        q=query,
        geocode='-22.9122,-43.2302,1km'
    ).items(10)
    # return api.user_timeline(
    #     screen_name=user_id,
    #     count=200,
    #     include_rts=False,
    #     tweet_mode='extended'
    # )


def format_haiku(haiku, user):
    first = post_process(haiku[1])
    second = post_process(haiku[2])
    third = post_process(haiku[3])
    sign = '\t - Infinite Loop Haikus'
    return f'@{user}\n{first}\n{second}\n{third}\n{sign}'


class HaikuListener(StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.retweeted:
            # Ignore retweets
            return
        logger.info(f'Processing tweet id {tweet.id}')
        if not tweet.truncated:
            text = tweet.text
        else:
            text = tweet.extended_tweet['full_text']
        text = pre_process(text)[0]
        haiku = extract_haiku(text, True)
        res = haiku[0]
        if (res):
            print(tweet.id)
            print(format_haiku(haiku, tweet.user.screen_name))
        if res & (not tweet.favorited):
            if tweet.in_reply_to_status_id is not None or \
                    tweet.user.id == self.me.id:
                # This tweet is a reply or I'm its author so, ignore it
                return
            try:
                tweet.favorite()
            except Exception as e:
                logger.error('Error favouriting haiku', exc_info=True)
        if res:
            try:
                haiku = format_haiku(haiku, tweet.user)
                self.api.update_status(haiku, tweet.id)
            except Exception as e:
                logger.error('Error replying to tweet', exc_info=True)

    def on_error(self, status):
        logger.error(status)


def main(api, hashtags):
    listener = HaikuListener(api)
    stream = Stream(api.auth, listener)
    stream.filter(track=hashtags, languages=['en'])


def alt(api):
    user_id = 'kanyewest'
    tweets = get_tweets(api, user_id)
    text = [pre_process(t.full_text)[0] for t in tweets]
    haikus = [extract_haiku(t) for t in text]
    tweets = [t for t, h in zip(tweets, haikus) if h[0]]
    haikus = [h for h in haikus if h[0]]
    pretty = format_haiku(haikus[3], tweets[3].user)
    print(pretty)


if __name__ == '__main__':
    hashtags = [
        'Python', 'Django', 'Node.js', 'GraphQL',
        'React', 'TypeScript', 'Java', 'Golang',
        'Kotlin', 'Serverless', 'AWS'
    ]
    main(create_api(), hashtags)
