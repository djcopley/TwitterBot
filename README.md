# TwitterBot

A simple program that replies to tweets. Response is generated using the CleverBot API.

# Usage

TwitterBot requires one positional argument to run, your twitter handle. Make sure to include the '@'
symbol.

Example: `python3 twitter_bot.py @yourhandle`

    positional arguments:
      user_handle           your twitter @handle
    
    optional arguments:
      -h, --help            show this help message and exit
      -m, --mute            disables console output of tweets
      -l {0,1,2}, --log {0,1,2}
                            change logging level

**Log Levels**
- 0 : logging is disabled (default)
- 1 : errors and program arguments are logged
- 2 : tweets (incoming and outgoing), errors, and program arguments are logged

# Installation

Generate API keys for [Twitter](https://apps.twitter.com) and [CleverBot](https://www.cleverbot.com/api/)

Create a credentials.py file and paste in the following (substituting your credentials into the empty fields):
    
    class Twitter:
        CONSUMER_KEY = ''
        CONSUMER_SECRET = ''
        ACCESS_TOKEN_KEY = ''
        ACCESS_TOKEN_SECRET = ''
    
    
    class CleverBot:
        API_KEY = ''

Install Dependencies: `pip3 install python-twitter CleverWrap`
