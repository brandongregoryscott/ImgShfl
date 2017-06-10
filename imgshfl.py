import random
import sys
from PIL import Image
import requests  # For opening the image from a URL
from io import BytesIO  # For opening the image from a URL
import re  # For regular expression matching the tweet text
import botconfig
import math

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
        rows = random.randint(3, 12)
        columns = random.randint(3, 12)
    row_step = float(img.height / rows)
    column_step = float(img.width / columns)

    partitions = list()

    # Iterate over the image and capture all of the partitions of the image
    for r in range(rows):
        for c in range(columns):
            left = math.ceil(c * column_step)
            upper = math.ceil(r * row_step)
            right = math.ceil((c + 1) * column_step)
            lower = math.ceil((r + 1) * row_step)
            bounding_box = (left, upper, right, lower)

            partition = img.crop(bounding_box)

            partitions.append(partition)

    # Now, iterate back over the image and paste a random partition
    for r in range(rows):
        for c in range(columns):
            left = math.ceil(c * column_step)
            upper = math.ceil(r * row_step)
            right = math.ceil((c + 1) * column_step)
            lower = math.ceil((r + 1) * row_step)
            bounding_box = (left, upper, right, lower)

            partition = partitions[random.randint(0, len(partitions) - 1)]
            partitions.remove(partition)

            img.paste(partition, bounding_box)
    return img

if __name__ == "__main__":
    main(sys.argv)
