import tweepy

from data.keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

twts = api.mentions_timeline()
print(api.me().screen_name)
# List of specific strings we want to check for in Tweets
t = ['@OniwaBansho Hello world!',
     '@OniwaBansho Hello World!',
     '@OniwaBansho Hello World!!!',
     '@OniwaBansho Hello world!!!',
     '@OniwaBansho Hello, world!',
     '@OniwaBansho Hello, World!',
     '@OniwaBansho hello world',]

for s in twts:
    for i in t:
        if i == s.text:
            #print(s.text)
           # print(s.user.screen_name)
            foo = api.statuses_lookup([s.id])
            #print(foo[0].text)
            try:
                api.update_status("@{} Hello!".format(s.user.screen_name), s.id)
            except tweepy.error.TweepError as e:
                print(e)