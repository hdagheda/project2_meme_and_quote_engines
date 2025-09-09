import random
import os
import requests

import tempfile
from flask import Flask, render_template, abort, request

from Ingestor.ingestor import Ingestor
from MemeEngine.meme_engine import MemeEngine

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # quote_files variable
    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    # images within the images images_path directory
    imgs = []
    for root, _, files in os.walk(images_path):
        for name in files:
            imgs.append(os.path.join(root, name))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user-defined meme """

    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    tmp_path = None
    try:
        resp = requests.get(image_url, timeout=10, verify=False)
        resp.raise_for_status()
        suffix = os.path.splitext(image_url)[1] or ".jpg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(resp.content)
            tmp_path = tmp.name

        path = meme.make_meme(tmp_path, body, author)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
