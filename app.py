import falcon
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.request import urlretrieve
from urllib.request import urlopen
from pathlib import Path
import datetime
import json


def in_cache(image_file_name):
    return Path(image_file_name).is_file()


def update_cache(image_location, image_name):
    urlretrieve(image_location, image_name)


def image_from_cache(image_name):
    # Is there a better way?
    image = Image.open(image_name)
    imgByteArr = BytesIO()
    image.save(imgByteArr, format='PNG')
    return imgByteArr.getvalue()


def daily_comic_from_hs(comic_path, comic_name):
    SCHEMA = 'https://'
    URL_HS = f'{SCHEMA}www.hs.fi'
    URL_COMIC = f'{URL_HS}{comic_path}'
    image_name = f'{datetime.date.today()}_{comic_name}.png'

    if not in_cache(image_name):
        html = urlopen(URL_COMIC)
        bsObj = BeautifulSoup(html, 'html.parser')
        image_link_url = URL_HS + \
            bsObj.select('.cartoon-content')[0].select('a')[0]['href']
        html = urlopen(image_link_url)
        bsObj = BeautifulSoup(html, 'html.parser')
        dirty_comic_url = bsObj.select('.scroller')[0].select('img')[
            0]['data-srcset']
        image_location = SCHEMA + dirty_comic_url.split()[0][2:] + '.webp'
        update_cache(image_location, image_name)

    return image_from_cache(image_name)


class QuoteResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps('It is sometimes an appropriate response '
                     'to reality to go insane.'
                     '    ~ Philip K. Dick')


class ViiviWagner(object):
    def on_get(self, req, resp):
        COMIC_PATH = '/viivijawagner/'
        try:
            resp.body = daily_comic_from_hs(COMIC_PATH, 'viivi-wagner')
            resp.content_type = falcon.MEDIA_PNG
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')


class FokIt(object):
    def on_get(self, req, resp):
        COMIC_PATH = '/nyt/fokit/'
        try:
            resp.body = daily_comic_from_hs(COMIC_PATH, 'fokit')
            resp.content_type = falcon.MEDIA_PNG
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')


class Fingerpori(object):
    def on_get(self, req, resp):
        COMIC_PATH = '/fingerpori/'
        try:
            resp.body = daily_comic_from_hs(COMIC_PATH, 'fingerpori')
            resp.content_type = falcon.MEDIA_PNG
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
quote = QuoteResource()
fingerpori = Fingerpori()
viivijawagner = ViiviWagner()
fokit = FokIt()

# request handlers for paths
app.add_route('/quote', quote)
app.add_route('/finger', fingerpori)
app.add_route('/viivi', viivijawagner)
app.add_route('/fokit', fokit)
