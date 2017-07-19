import tweepy as tw
import time

from keys import keys
from restaurant_picker import pick_restaurant

class TwitterBot(object):
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret, max_id):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.max_id = max_id

        # Authorize app with twitter
        self.auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tw.API(self.auth)
        print('Authorized')

    def run_bot(self):
        print('running')
        while(True):
            # Get a list of all the tweets where this account is mentioned
            twts = self.api.mentions_timeline(since_id=self.max_id)

            # Get accounts current screen name
            my_screen_name = self.api.me().screen_name

            # Phrases to recognize
            phrase = ['@{} Where to eat?'.format(my_screen_name),
                      '@{} where to eat?'.format(my_screen_name),
                      ]

            for s in twts:
                for i in phrase:
                    if i == s.text:
                        print('Found something!')
                        tweeters_screen_name = s.user.screen_name
                        self.max_id = s.id
                        try:
                            self.api.update_status('@{} You should eat at'
                                                   ' {}'.format(tweeters_screen_name,
                                                                pick_restaurant()),
                                                                s.id)
                            print('did something')
                        except tw.error.TweepError as e:
                            print(e)
            time.sleep(300)


if __name__ == '__main__':
    foodbot = TwitterBot(keys['consumer_key'], keys['consumer_secret'],
                         keys['access_token'], keys['access_token_secret'], 887804597154312191)
    foodbot.run_bot()

