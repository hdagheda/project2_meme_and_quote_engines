import os
import random
import argparse
import configparser

from Ingestor import Ingestor
from MemeEngine.meme_engine import MemeEngine
from QuoteEngine import QuoteModel


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    config = configparser.ConfigParser()
    config.read('./config.ini')
    category = config.get('DEFAULT', 'category', fallback='sadhguru')

    if path is None:
        if category == 'sadhguru':
            images = "./_data/photos/sadhguru/"
        else:
            images = "./_data/photos/dog/"

        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        if category == 'sadhguru':
            quote_files = ['./_data/SadhguruQuotes/SadhguruQuotesTXT.txt',
                           './_data/SadhguruQuotes/SadhguruQuotesCSV.csv']
        else:
            quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                           './_data/DogQuotes/DogQuotesDOCX.docx',
                           './_data/DogQuotes/DogQuotesPDF.pdf',
                           './_data/DogQuotes/DogQuotesCSV.csv']

        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(
        description="Generate a meme from an image and an optional quote."
    )
    parser.add_argument(
        "--path",
        type=str,
        nargs=1,
        default=None,
        help="Path to an image file."
    )
    parser.add_argument(
        "--body",
        type=str,
        default=None,
        help="Quote body to add to the image."
    )
    parser.add_argument(
        "--author",
        type=str,
        default=None,
        help="Quote author to add to the image."
    )
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
