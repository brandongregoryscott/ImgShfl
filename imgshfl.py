import random
import sys
from PIL import Image
import requests  # For opening the image from a URL
from io import BytesIO  # For opening the image from a URL
import re  # For regular expression matching the tweet text
import botconfig
import math

def factorize(num):
    factors = list()
    for i in range(1, int(num / 3)):
        if num % i == 0 and i != 1 and i != num:
            factors.append(i)
    return factors

def main(argv):
    # Tweet object is passed into this module
    tweet = argv

    # Open the image from the URL
    response = requests.get(tweet['entities']['media'][0]['media_url'])
    img = Image.open(BytesIO(response.content))

    # Strip out the bot mention in the tweet text, and strip the extra whitespace
    tweet_text = str(tweet['text']).replace(botconfig.botMention, "").strip()

    pattern = re.compile("[0-9]+[x][0-9]+")

    if pattern.match(tweet_text):
        # Parse out the rows/columns from the tweet text if the pattern matches
        size_string = tweet_text.split()[0]
        rows = int(size_string.split("x")[0])
        columns = int(size_string.split("x")[1])
    else:
        row_factors = factorize(img.height)
        column_factors = factorize(img.width)
        if len(row_factors) > 0:
            rows = random.choice(row_factors)
        else:
            rows = random.randint(3, 25)
        if len(column_factors) > 0:
            columns = random.choice(column_factors)
        else:
            columns = random.randint(3, 25)

        row_step = img.height / rows
        column_step = img.width / columns

    partitions = list()

    # Iterate over the image and capture all of the partitions of the image
    for r in range(rows):
        for c in range(columns):
            left = math.floor(c * column_step)
            upper = math.floor(r * row_step)
            right = math.floor((c + 1) * column_step)
            lower = math.floor((r + 1) * row_step)
            bounding_box = (left, upper, right, lower)

            partition = img.crop(bounding_box)

            partitions.append(partition)
    # Now, iterate back over the image and paste a random partition
    new_img = Image.new('RGBA', img.size)
    for r in range(rows):
        for c in range(columns):
            left = math.floor(c * column_step)
            upper = math.floor(r * row_step)
            partition = random.choice(partitions)
            partitions.remove(partition)

            new_img.paste(partition, (left, upper))
    new_img.show()
    return new_img

if __name__ == "__main__":
    main(sys.argv)
