# sarjis
Extract daily comics from different sources

https://github.com/falconry/falcon


### installing and running 

#### without docker

- clone repo and `cd sarjis`
- create and activate virtual environment: `python3 -m venv venv; source venv/bin/activate`
- install modules: `pip install -r requirements.txt`
- start server: `gunicorn app:app`
- test in terminal: `curl localhost:8000/quotes`

#### using docker 

- clone repo and `cd sarjis`
- build docker image: `docker build . -t sarjis`
- run image: ´docker run -p 8000:8000 sarjis´
