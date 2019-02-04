# https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3

FROM python:3.6-alpine

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000

# http://docs.gunicorn.org/en/stable/run.html
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
