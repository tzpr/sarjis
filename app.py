import falcon
import requests
from bs4 import BeautifulSoup
import os



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
            comic_url = dirty_comic_url.split()[0][2:]
            schema = 'https://'
            res = requests.get(schema + comic_url)
            res.raise_for_status()
            # TODO: Fix me, I am wrong.
            resp.status = falcon.HTTP_200  # This is the default status
            resp.stream = open(res.text, 'rb')
            resp.stream_len = os.path.getsize(res.text)
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

