"""
The goal of version 2.0 is to reply directly to threads where you are mentioned.
"""
import twitter
import re
from cleverwrap import CleverWrap
from credentials import Twitter, CleverBot

api = twitter.Api(
    consumer_key=Twitter.CONSUMER_KEY,
    consumer_secret=Twitter.CONSUMER_SECRET,
    access_token_key=Twitter.ACCESS_TOKEN_KEY,
    access_token_secret=Twitter.ACCESS_TOKEN_SECRET
)

cleverbot = CleverWrap(api_key=CleverBot.API_KEY)


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
    try:
        # Be sure to replace @djrcopley with YOUR twitter handle
        for tweet in api.GetStreamFilter(track=['@djrcopley']):
            response = cleverbot.say(strip_user_handles(tweet['text']))
            send_tweet(tweet['user']['screen_name'], response)

            print('Tweet from @{}'.format(tweet['user']['screen_name']))
            print(tweet['text'])
            print('Reply: {}'.format(response))

    except KeyboardInterrupt:
        print('\nQuitting')
