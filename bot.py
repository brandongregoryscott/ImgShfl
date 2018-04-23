import io
import random
import logging
import sys
import ast
import os
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
        self.config['api_key'] = os.environ['API_KEY']
        self.config['api_secret'] = os.environ['API_SECRET']
        self.config['access_key'] = os.environ['ACCESS_KEY']
        self.config['access_secret'] = os.environ['ACCESS_SECRET']

        ######################################
        # SEMI-OPTIONAL: OTHER CONFIG STUFF! #
        ######################################

        # how often to tweet, in seconds
        self.config['tweet_interval'] = ast.literal_eval(os.getenv('TWEET_INTERVAL', 60 * 30))  # default: 30 minutes

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = ast.literal_eval(os.getenv('REPLY_DIRECT_MENTION_ONLY', False))

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = ast.literal_eval(os.getenv('REPLY_FOLLOWERS_ONLY', False))

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = ast.literal_eval(os.getenv('AUTOFAV_MENTIONS', False))

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = ast.literal_eval(os.getenv('AUTOFAV_KEYWORDS', list()))

        # follow back all followers?
        self.config['autofollow'] = ast.literal_eval(os.getenv('AUTOFOLLOW', False))

        ###########################################
        # CUSTOM: your bot's own config variables! #
        ###########################################

        self.config['bots'] = ast.literal_eval(os.getenv('BOTS', list()))
        self.config['tags'] = ast.literal_eval(os.getenv('TAGS', list()))
        self.config['responses'] = ast.literal_eval(os.environ['RESPONSES'])

        if os.environ.get('LAST_MENTION_ID') is not None:
            self.state['last_mention_id'] = ast.literal_eval(os.environ['LAST_MENTION_ID'])
        if os.environ.get('LAST_MENTION_TIME') is not None:
            self.state['last_mention_time'] = ast.literal_eval(os.environ['LAST_MENTION_TIME'])

    def on_scheduled_tweet(self):
        return
        mention_user = random.choice(self.config['bots'])
        text = random.choice(self.config['tags'])
        img = module.original()
        self.post_tweet(".@{0} {1}".format(mention_user, text), media=convert_image_to_bytes(img))

    def on_mention(self, tweet, prefix):
        reply_user = tweet['user']['screen_name']
        if 'media' not in tweet['entities'].keys():
                pass
        else:
            reply_img = module.main(tweet)
            text = random.choice(self.config['responses'])
            while not self.post_tweet(".@{0} {1}".format(reply_user, text), reply_to=tweet, media=convert_image_to_bytes(reply_img)):
                pass

    @ignore
    def on_timeline(self, tweet, prefix):
        pass

if __name__ == '__main__':
    bot = Bot()
    bot.run()
