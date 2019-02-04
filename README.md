# sarjis
Extract daily comics from different sources

https://github.com/falconry/falcon


### installing and running

- clone repo and `cd sarjis`
- create and activate virtual environment: `python3 -m venv venv; source venv/bin/activate`
- install modules: `pip install -r requirements.txt`
- start server: `gunicorn app:app`
- test in terminal: `curl localhost:8000/quotes`
