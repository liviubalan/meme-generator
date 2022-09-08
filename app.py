from flask import Flask, render_template, abort, request
from QuoteEngine.Classes import Ingestor, MemeEngine
import os
import random
import requests

app = Flask(__name__)
meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for quote_file in quote_files:
        quotes.extend(Ingestor.parse(quote_file))

    images_path = "./_data/photos/dog/"
    imgs = [images_path + file for file in os.listdir(images_path)]

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
    """ Create a user defined meme """
    data = request.form
    url = data['image_url']
    extension = Ingestor.extension(url)
    tmp_file_name = f"./_data/photos/generated_meme.{extension}"
    tmp_file = open(tmp_file_name, 'wb')
    req = requests.get(url)
    tmp_file.write(req.content)

    path = meme.make_meme(tmp_file_name, data['body'], data['author'])
    os.remove(tmp_file_name)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        print(f"Exception encountered: {e}")
