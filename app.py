import falcon
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO
import msgpack



# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class QuoteResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nIt is sometimes an appropriate response '
                     'to reality to go insane.\n'
                     '\n'
                     '    ~ Philip K. Dick\n\n')


class Fingerpori(object):
    def on_get(self, req, resp):        
        try:
            finger_page_url = 'https://www.hs.fi/fingerpori/'
            res = requests.get(finger_page_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            # 1. div class cartoon-content > 1. img > data-srcset
            dirty_comic_url = soup.select('.cartoon-content')[0].select('img')[0]['data-srcset']
            schema = 'https://'
            comic_url = schema + dirty_comic_url.split()[0][2:]
            print('Comic ULR:', comic_url)
            res = requests.get(comic_url)
            i = Image.open(BytesIO(res.content))
            i.save('fingerpori.png')  # image is saved to a file
            # TODO: return the image
            print('TESTING the image:', i)
            #resp.data = msgpack.packb(i, use_bin_type=True)  # TypeError: can not serialize 'JpegImageFile' object
            #resp.content_type = falcon.MEDIA_MSGPACK
            resp.status = falcon.HTTP_200  # This is the default status
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
quotes = QuoteResource()
fingerpori = Fingerpori()

# things will handle all requests to the '/things' URL path
app.add_route('/quotes', quotes)
app.add_route('/finger', fingerpori)

