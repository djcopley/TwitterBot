#!/usr/bin/env python3
"""
Code by Daniel Copley
Source @ GitHub.com/djcopley
Version 1.0
"""

import twitter
import re
import argparse
from cleverwrap import CleverWrap
from credentials import Twitter, CleverBot

api = twitter.Api(
    consumer_key=Twitter.CONSUMER_KEY,
    consumer_secret=Twitter.CONSUMER_SECRET,
    access_token_key=Twitter.ACCESS_TOKEN_KEY,
    access_token_secret=Twitter.ACCESS_TOKEN_SECRET
)

cleverbot = CleverWrap(api_key=CleverBot.API_KEY)

# Argument Parsing
parser = argparse.ArgumentParser(description='A bot that automatically responds to tweets.',
                                 prog='Twitter Bot')
parser.add_argument('twitter_handle', help='your twitter @handle', type=str)
parser.add_argument('-r', '--reply_to_thread', help='toggles reply to thread where mentioned', action='store_true',
                    default=False)
parser.add_argument('-q', '--quiet', help='disables console output of non-errors', action='store_true', default=False)
parser.add_argument('-l', '--log', help='change logging level', type=int, choices=[0, 1, 2], default=0)

arguments = parser.parse_args()

# Logging Setup
log_level = {0: None, 1: logging.ERROR, 2: logging.INFO}[arguments.log]  # File log level
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR if arguments.quiet else logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

if log_level:  # Set up file handler if log level is specified
    file_handler = logging.FileHandler('twitter_bot.log')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def send_tweet(handle, text, tweet_id=None):
    try:
        logger.debug('send_tweet: id={}, handle={}, text={}'.format(tweet_id, handle, text))
        api.PostUpdate('@{} {}'.format(handle, text), in_reply_to_status_id=tweet_id)

    except Exception:
        logger.error('Failed to send tweet', exc_info=True)


def strip_user_handles(text):
    """Function strips user handles from incoming tweet"""
    pattern = r'\B@\w+ *'
    result = re.sub(pattern, '', text)
    logger.debug('strip_user_handles: input:{}, output:{}'.format(text, result))
    return result


if __name__ == '__main__':
    print('~ TwitterBot is now running ~\n')
    try:
        for tweet in api.GetStreamFilter(track=[str(arguments.twitter_handle)]):
            response = cleverbot.say(strip_user_handles(tweet['text']))
            send_tweet(tweet['user']['screen_name'], response,
                       tweet_id=tweet['id'] if arguments.reply_to_thread else None)

            logger.debug('Tweet: {}'.format(tweet))
            logger.info('Incoming tweet from {}: {}'.format(tweet['user']['screen_name'], tweet['text']))
            logger.info('Reply: {}'.format(response))

    except KeyboardInterrupt:
        print('\n~ Quitting ~')
