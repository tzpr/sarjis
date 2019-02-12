import falcon
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.request import urlretrieve
from urllib.request import urlopen
from pathlib import Path
import datetime


def in_cache(image_file_name):
    return Path(image_file_name).is_file()


def update_cache(image_location, image_name):
    urlretrieve(image_location, image_name)


def image_from_cache(image_name):
    # TODO is there a better way?
    image = Image.open(image_name)
    imgByteArr = BytesIO()
    image.save(imgByteArr, format='PNG')
    return imgByteArr.getvalue()


def daily_comic_from_hs(comimc_path, comic_name):
    SCHEMA = 'https://'
    URL_HS = SCHEMA + 'www.hs.fi'
    URL_COMIC = URL_HS + comimc_path
    image_name = str(datetime.date.today()) + '_' + comic_name + '.png'

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


class Dilbert(object):
    def on_get(self, req, resp):
        SCHEMA = 'https://'
        URL_DILBERT = SCHEMA + 'dilbert.com'
        URL_COMIC = URL_DILBERT + '/strip/' + str(datetime.date.today())
        image_name = str(datetime.date.today()) + '_dilbert.png'

        if not in_cache(image_name):
            html = urlopen(URL_COMIC)
            bsObj = BeautifulSoup(html, 'html.parser')
            dirty_comic_url = bsObj.select(
                '.img-comic-container')[0].select('img')[0]['src']
            image_location = SCHEMA + dirty_comic_url[2:]
            update_cache(image_location, image_name)

        try:
            resp.body = image_from_cache(image_name)
            resp.content_type = falcon.MEDIA_PNG
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')


class QuoteResource(object):
    def on_get(self, req, resp):
        print('Testing magik:', req.params.get('magik'))
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nIt is sometimes an appropriate response '
                     'to reality to go insane.\n'
                     '\n'
                     '    ~ Philip K. Dick\n\n')


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
dilbert = Dilbert()

# request handlers for paths
app.add_route('/quote', quote)
app.add_route('/finger', fingerpori)
app.add_route('/viivi', viivijawagner)
app.add_route('/fokit', fokit)
app.add_route('/dilbert', dilbert)
