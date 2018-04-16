#!/usr/bin/env python3
"""
Code by Daniel Copley
Source @ GitHub.com/djcopley
Version 0.1.2-beta

# TODO - Reply directly to thread
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
parser.add_argument('-q', '--quiet', help='disables console output of non-errors', action='store_true', default=False)
parser.add_argument('-l', '--log', help='change logging level', type=int, choices=[0, 1, 2], default=0)

arguments = parser.parse_args()

# Logging Setup
logging.basicConfig(level=logging.INFO)

log_level = {0: None, 1: logging.ERROR, 2: logging.INFO}[arguments.log]
logger = logging.getLogger(__name__)

if log_level:  # Set up file handler if log level is specified
    logger.setLevel(log_level)

    handler = logging.FileHandler('twitter_bot.log')
    handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def send_tweet(handle, text):
    try:
        logger.debug('send_tweet({}, {})'.format(handle, text))
        api.PostUpdate('@{} {}'.format(handle, text))

    except Exception:
        logger.error('Failed to send tweet', exc_info=True)


def strip_user_handles(text):
    """Function strips user handles from incoming tweet"""
    pattern = r'\B@\w+ *'
    result = re.sub(pattern, '', text)
    logger.debug('strip_user_handles({}) --> {}'.format(text, result))
    return result


if __name__ == '__main__':
    print('~ TwitterBot is now running ~\n')
    try:
        for tweet in api.GetStreamFilter(track=[str(arguments.twitter_handle)]):
            response = cleverbot.say(strip_user_handles(tweet['text']))
            send_tweet(tweet['user']['screen_name'], response)

            if not arguments.quiet:
                logger.info('Incoming tweet: {}'.format(tweet))
                logger.info('Reply: {}'.format(response))

    except KeyboardInterrupt:
        print('\n~ Quitting ~')
