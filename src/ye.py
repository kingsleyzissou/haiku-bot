import logging
import numpy as np
from tweepy import Stream, StreamListener
from twitter import create_api
from pre_processing import pre_process
from post_processing import post_process
from haiku_detection import extract_haiku

logger = logging.getLogger()


def get_tweets(api, user_id):
    return api.user_timeline(
        screen_name=user_id,
        count=200,
        include_rts=False,
        tweet_mode='extended'
    )


def format_haiku(haiku):
    first = post_process(haiku[1])
    second = post_process(haiku[2])
    third = post_process(haiku[3])
    sign = '\t - haikus_by_ye'
    return f"@kanyewest\n{first}\n{second}\n{third}\n{sign}"


class YeListener(StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.retweeted:
            # Ignore retweets
            return
        logger.info(f"Processing tweet id {tweet.id}")
        text = pre_process(tweet.full_text)
        haiku = extract_haiku(text, True)
        res = haiku[0]
        if res & (not tweet.favorited):
            if tweet.in_reply_to_status_id is not None or \
                    tweet.user.id == self.me.id:
                # This tweet is a reply or I'm its author so, ignore it
                return
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error favouriting haiku", exc_info=True)
        if res:
            try:
                haiku = format_haiku(haiku)
                api.update_status(haiku, tweet.id)
            except Exception as e:
                logger.error("Error replying to tweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)


if __name__ == "__main__":
    listener = StreamListener()
    api = create_api()
    stream = Stream(api.auth, listener)
    stream.filter(follow=['kanyewest'])
