import falcon
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO



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


class ViiviWagner(object):
    def on_get(self, req, resp): 
        resp.status = falcon.HTTP_200
        resp.body = '\nDaily Viivi and Wagner\n\n'


class FokIt(object):
    def on_get(self, req, resp): 
        resp.status = falcon.HTTP_200
        resp.body = '\nDaily Fok_It\n\n'        


class Fingerpori(object):
    def on_get(self, req, resp): 
        DEBUG = False
        SCHEMA = 'https://'
        URL_HS = SCHEMA + 'www.hs.fi'
        URL_FINGERPORI = URL_HS + '/fingerpori/'

        try:
            res = requests.get(URL_FINGERPORI)
            soup = BeautifulSoup(res.text, 'html.parser')
            image_link_url = URL_HS + soup.select('.cartoon-content')[0].select('a')[0]['href']
            
            if (DEBUG):
                print('image_link_url: ', image_link_url)

            res = requests.get(image_link_url)
            soup = BeautifulSoup(res.text, 'html.parser')

            dirty_comic_url = soup.select('.scroller')[0].select('img')[0]['data-srcset']
            comic_url = SCHEMA + dirty_comic_url.split()[0][2:] + '.webp'

            if (DEBUG):
                print('imgage url:', comic_url)

            # TODO: check and maybe refactor
            res = requests.get(comic_url)
            image = Image.open(BytesIO(res.content))
            imgByteArr = BytesIO()
            image.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            resp.body = imgByteArr
            resp.content_type = falcon.MEDIA_PNG
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500
            resp.body('ERROR ERROR')


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
quotes = QuoteResource()
fingerpori = Fingerpori()
viiviw = ViiviWagner()
fokit = FokIt()

# request handlers for paths
app.add_route('/quotes', quotes)
app.add_route('/finger', fingerpori)
app.add_route('/viiviw', viiviw)
app.add_route('/fokit', fokit)