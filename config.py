#!/usr/bin/python

import os.path
import json
import re

FILE_CONFIG = "config.json"
END_POINT = "http://api.escuchable.com/"
CATEGORY = 0
PODCAST = 0
TOKEN = ""
LOGGED = False

if (os.path.isfile(FILE_CONFIG)):
    LOGGED = True
    file = open(FILE_CONFIG, "r")
    config = json.loads(file.read())
    file.close()
    TOKEN = config['token']

    if ('category' in config):
        CATEGORY = config['category']
    if ('podcast' in config):
        PODCAST = config['podcast']


def saveConfig(key, value):
    if (os.path.isfile(FILE_CONFIG)):
        file = open(FILE_CONFIG, "r")
        config = json.loads(file.read())
        file.close()
    else:
        config = {}

    config[key] = value

    file = open(FILE_CONFIG, "w+")
    file.write(json.dumps(config))
    file.close()

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext