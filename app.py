import time

import redis
from flask import Flask
from os import environ


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
mode = 'production' if environ.get('FLASK_ENV') is None else environ.get('FLASK_ENV')


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello from Docker Fan! I have been seen {} times.\n Refresh it again.'.format(count)


@app.route('/hello')
def index():
    return "Hello, this is a hello method!\n"


@app.route('/name/<name>')
def get_name(name):
    return "Hello ," + name + " from " + str(mode) + ".\n"
