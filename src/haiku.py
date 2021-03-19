import logging
import numpy as np
import time
from tweepy import Cursor, Stream, StreamListener
from twitter import create_api
from pre_processing import pre_process
from post_processing import post_process
from haiku_detection import extract_haiku

logger = logging.getLogger()


def format_haiku(haiku):
    first = post_process(haiku[1])
    second = post_process(haiku[2])
    third = post_process(haiku[3])
    sign = '\t - Infinite Loop Haikus'
    return f'{first}\n{second}\n{third}\n{sign}'


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
        if res & (not tweet.favorited):
            if tweet.in_reply_to_status_id is not None or \
                    tweet.user.id == self.me.id:
                # This tweet is a reply or I'm its author so, ignore it
                return
        if res:
            try:
                haiku = format_haiku(haiku)
                logger.info('Found a haiku')
                self.api.update_status(haiku)
                time.sleep(60 * 120)
            except Exception as e:
                logger.error('Error replying to tweet', exc_info=True)

    def on_error(self, status):
        logger.error(status)


def main(api, hashtags):
    listener = HaikuListener(api)
    stream = Stream(api.auth, listener)
    stream.filter(track=hashtags, languages=['en'])


if __name__ == '__main__':
    topics = [
        'Python', 'Django', 'Node.js', 'GraphQL',
        'React.js', 'TypeScript', 'Java', 'Golang',
        'Kotlin', 'Serverless', 'AWS', 'Vue', 'Nuxt',
        'Next.js', 'Nuxt.js', 'Programming', 'Debugging'
    ]
    api = create_api()
    main(create_api(), topics)
