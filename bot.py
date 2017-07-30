import io
import random
import logging
import sys

from twitterbot import TwitterBot, ignore

import imgshfl as module

def convert_image_to_bytes(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes

class Bot(TwitterBot):
    def bot_init(self):
        ############################
        # REQUIRED: LOGIN DETAILS! #
        ############################
        self.config['api_key'] = ''
        self.config['api_secret'] = ''
        self.config['access_key'] = ''
        self.config['access_secret'] = ''

        ######################################
        # SEMI-OPTIONAL: OTHER CONFIG STUFF! #
        ######################################

        # how often to tweet, in seconds
        self.config['tweet_interval'] = 60 * 60  # default: 30 minutes

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        self.config['tweet_interval_range'] = (45 * 60, 75 * 60)

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = False

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False

        ###########################################
        # CUSTOM: your bot's own config variables! #
        ###########################################

        self.config['bots'] = ['imgavgbot', 'artyabstract', 'artycrush', 'artycurve', 'abstractedbot']
        self.config['tags'] = ['Here, take this image - it\'s your problem now!',
                               'I did the best I could. Can you take it from here?',
                               'Here you go.']
        self.config['responses'] = ['Here, take this image - you wanted it!',
                                    'I did the best I could.',
                                    'Is this what you wanted?',
                                    'This image is pretty shuffled now.',
                                    'Jumbled, at best.',
                                    'All shuffled up, this is what your image looks like.',
                                    'Everything feels a little jumbled now.']

    def on_scheduled_tweet(self):
        return
        mention_user = random.choice(self.config['bots'])
        text = random.choice(self.config['tags'])
        img = module.original()
        self.post_tweet(".@{0} {1}".format(mention_user, text), media=convert_image_to_bytes(img))

    def on_mention(self, tweet, prefix):
        reply_user = tweet['user']['screen_name']
        if 'media' not in tweet['entities'].keys():
            self.post_tweet(".@{0} Sorry, I don't see an image.".format(reply_user), reply_to=tweet)
        else:
            reply_img = module.main(tweet)
            text = random.choice(self.config['responses'])
            self.post_tweet(".@{0} {1}".format(reply_user, text), reply_to=tweet,
                            media=convert_image_to_bytes(reply_img))

    @ignore
    def on_timeline(self, tweet, prefix):
        pass

if __name__ == '__main__':
    bot = Bot()
    bot.run()
