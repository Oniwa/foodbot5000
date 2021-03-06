import tweepy as tw
import json
from random import randint
import logging

from data.keys import keys


class TwitterBot(object):
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.max_id = []
        self.restaurants = []
        self.json_data = []

        # Authorize app with twitter
        self.auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tw.API(self.auth)

        self.log = logging.getLogger('Logbot 5000')
        self.log.setLevel(logging.INFO)
        fh = logging.FileHandler('./data/error.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.log.addHandler(fh)

    def load_json(self):
        with open('./data/data.json') as json_file:
            self.json_data = json.load(json_file)

        self.max_id = self.json_data['max_tweet_id']
        self.restaurants = self.json_data['restaurants']

    def pick_restaurant(self):
        return self.restaurants[randint(0, len(self.restaurants) - 1)]

    def run_bot(self):
        self.log.info('Program started')
        try:
            self.load_json()
        except FileNotFoundError as e:
            self.log.exception("JSON file not found.")
            return
        except KeyError as e:
            self.log.exception('JSON key not found in file')
            return

        # Get a list of all the tweets where this account is mentioned
        twts = self.api.mentions_timeline(since_id=self.max_id)

        # Get accounts current screen name
        my_screen_name = self.api.me().screen_name

        # Phrases to recognize
        phrase = ['@{} Where to eat?'.format(my_screen_name),
                  '@{} where to eat?'.format(my_screen_name),
                  ]

        # Search all new tweets to see if they match the phrase
        for s in twts:
            for i in phrase:
                if i == s.text:
                    # If match reply to the tweet and set max_id so we don't
                    # reply to old tweets
                    tweeters_screen_name = s.user.screen_name
                    self.max_id = s.id
                    try:
                        restaurant = self.pick_restaurant()
                        self.api.update_status('@{} You should eat at'
                                               ' {}'.format(tweeters_screen_name,
                                                            restaurant),
                                                            s.id)
                        self.log.info(f'{tweeters_screen_name} sent tweet '
                                      f'{s.id} and was given restaurant '
                                      f'{restaurant}')
                    except tw.error.TweepError as e:
                        self.log.exception("Error updating twitter status")

        # If any tweets where updated update the JSON file with new max tweet id
        if self.json_data['max_tweet_id'] != self.max_id:
            self.json_data['max_tweet_id'] = self.max_id
            with open('./data/data.json', 'w') as outfile:
                json.dump(self.json_data, outfile, indent=4)
            self.log.info(f'Max ID is {self.max_id}')
        self.log.info('Program finished')


if __name__ == '__main__':
    foodbot = TwitterBot(keys['consumer_key'], keys['consumer_secret'],
                         keys['access_token'], keys['access_token_secret'])
    foodbot.run_bot()

