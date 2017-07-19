import tweepy as tw
import time

from keys import keys
from restaurant_picker import pick_restaurant

# Get Keys from the secret key file
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

# Authorize app with twitter
auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth)

# Get a list of all the tweets where this account is mentioned
twts = api.mentions_timeline()

# Get accounts current screen name
my_screen_name = api.me().screen_name

# Phrases to recognize
phrase = ['@{} Where to eat?'.format(my_screen_name),
          '@{} where to eat?'.format(my_screen_name),
          ]

for s in twts:
    for i in phrase:
        if i == s.text:
            tweeters_screen_name = s.user.screen_name
            max_id = s.id
            try:
                api.update_status('@{} You should eat at'
                                  ' {}'.format(tweeters_screen_name,
                                               pick_restaurant()), s.id)
            except tw.error.TweepError as e:
                print(e)
