import random
import sys
from PIL import Image, ImageDraw
import requests  # For opening the image from a URL
from io import BytesIO  # For opening the image from a URL
import re  # For regular expression matching the tweet text
import math

def factorize(num):
    factors = list()
    for i in range(1, int(num / 3)):
        if num % i == 0 and i != 1 and i != num:
            factors.append(i)
    return factors


def shuffle_img(img, rows, columns):
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
    return new_img


def main(argv):
    # Tweet object is passed into this module
    tweet = argv

    # Open the image from the URL
    response = requests.get(tweet['entities']['media'][0]['media_url'])
    img = Image.open(BytesIO(response.content))

    # Strip out the bot mention in the tweet text, and strip the extra whitespace
    tweet_text = str(tweet['text']).replace("@imgshflbot", "").strip()

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
            rows = random.randint(3, 15)
        if len(column_factors) > 0:
            columns = random.choice(column_factors)
        else:
            columns = random.randint(3, 15)

    img = shuffle_img(img, rows, columns)
    return img

def original():
    img_size = random.choice([(1920, 1080), (1080, 1920), (2000, 2000), (2560, 2048), (2048, 2560)])
    palette = list()
    base_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 100))
    for z in range(random.randint(500, 1000)):
        palette.append((base_color[0] + random.randint(-50, 50), base_color[1], base_color[2] + random.randint(-50, 50)))

    img = Image.new('RGB', img_size, random.choice(palette))
    draw = ImageDraw.Draw(img)

    points = list()
    for x in range(-int(img.width / 2), int(img.width * 2), random.randint(20, 50)):
        for y in range(-int(img.height / 2), int(img.height * 2), random.randint(20, 50)):
            points.append((x, y))
    for i in range(random.randint(100, 200)):
        start_degrees = random.randint(0, 180)
        end_degrees = random.randint(start_degrees, 360)
        point_sample = random.sample(points, 2)
        draw.pieslice(xy=point_sample, start=start_degrees, end=end_degrees, fill=random.choice(palette))

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

    img = shuffle_img(img, rows, columns)
    img.save("/out/" + str(random.randint(int(sys.maxsize / 4), sys.maxsize)) + ".png")
    return img

if __name__ == "__main__":
    main(sys.argv)
