import falcon
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.request import urlretrieve
from urllib.request import urlopen
from pathlib import Path
import datetime


def scrape_daily_comic_strip(comimc_path, img_name):
    SCHEMA = 'https://'
    URL_HS = SCHEMA + 'www.hs.fi' 
    URL_COMIC = URL_HS + comimc_path

    image_file_name = str(datetime.date.today()) + '_' + img_name + '.png'

    # check if img exists
    if not Path(image_file_name).is_file():
        html = urlopen(URL_COMIC)
        bsObj = BeautifulSoup(html, 'html.parser')
        image_link_url = URL_HS + bsObj.select('.cartoon-content')[0].select('a')[0]['href']

        html = urlopen(image_link_url)
        bsObj = BeautifulSoup(html, 'html.parser')
        dirty_comic_url = bsObj.select('.scroller')[0].select('img')[0]['data-srcset']
        image_location = SCHEMA + dirty_comic_url.split()[0][2:] + '.webp'

        urlretrieve(image_location, image_file_name)

    # TODO check if there's a better way
    image = Image.open(image_file_name)
    imgByteArr = BytesIO()
    image.save(imgByteArr, format='PNG')
    return imgByteArr.getvalue()


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
            resp.body = scrape_daily_comic_strip(COMIC_PATH, 'viivi-wagner')
            resp.content_type = falcon.MEDIA_PNG
           # resp.send_header("Content-length", img_size)
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')   


class FokIt(object):
    def on_get(self, req, resp):
        COMIC_PATH = '/nyt/fokit/'
        try:
            resp.body = scrape_daily_comic_strip(COMIC_PATH, 'fokit')
            resp.content_type = falcon.MEDIA_PNG
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')                


class Fingerpori(object):
    def on_get(self, req, resp): 
        COMIC_PATH = '/fingerpori/'
        try:
            resp.body = scrape_daily_comic_strip(COMIC_PATH, 'fingerpori')
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