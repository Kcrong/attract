# -*-coding: utf-8 -*-

from flask import Flask
import random
import string

app = Flask(__name__)


def randomkey(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


app.secret_key = randomkey(35)

app.static_folder = 'static'
app.static_url_path = 'static'
app.template_folder = 'static'
