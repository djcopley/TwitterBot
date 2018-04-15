#!/usr/bin/env python3
"""
Code by Daniel Copley
Source @ GitHub.com/djcopley
Version 0.1.2-beta
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

# TODO Setup logger
logger = logging.Logger('')


def send_tweet(handle, text):
    try:
        api.PostUpdate('@{} {}'.format(handle, text))

    except Exception as error:
        print('An error occurred: {}'.format(error))


def strip_user_handles(text):
    """Function strips user handles from incoming tweet"""
    pattern = r'\B@\w+ *'
    return re.sub(pattern, '', text)


if __name__ == '__main__':
    print('~ TwitterBot is now running ~')
    try:
        for tweet in api.GetStreamFilter(track=[str(arguments.twitter_handle)]):
            response = cleverbot.say(strip_user_handles(tweet['text']))
            send_tweet(tweet['user']['screen_name'], response)

            if not arguments.quiet:
                print('Tweet from @{}'.format(tweet['user']['screen_name']))
                print(tweet['text'])
                print('Reply: {}'.format(response))

    except KeyboardInterrupt:
        print('\n~ Quitting ~')
