#/usr/bin/env python

try:
    from flask import Flask
except ImportError:
    print "\n[X] Please install Flask:"
    print "   $ pip install flask\n"
    exit()

from optparse import OptionParser
from wordpot.logger import *
from werkzeug.routing import BaseConverter
from wordpot.plugins_manager import PluginsManager
import os

# ---------------
# Regex Converter
# ---------------

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# -------
# Options
# -------

REQUIRED_OPTIONS = {
        'HOST':  '127.0.0.1',
        'PORT':  '80',
        'THEME': 'twentyeleven',
        'BLOGTITLE': 'Random Rambling',
        'AUTHORS': ['admin']
        }


def parse_options():
    usage = "usage: %prog [options]"

    parser = OptionParser(usage=usage)
    parser.add_option('--host', dest='HOST', help='Host address')
    parser.add_option('--port', dest='PORT', help='Port number')
    parser.add_option('--title', dest='BLOGTITLE', help='Blog title')
    parser.add_option('--theme', dest='THEME', help='Default theme name')
    parser.add_option('--plugins', dest='PLUGINS', help='Fake installed plugins')
    parser.add_option('--themes', dest='THEMES', help='Fake installed themes')
    parser.add_option('--ver', dest='VERSION', help='Wordpress version')

    (options, args) = parser.parse_args()
    
    for opt, val in options.__dict__.iteritems():
        if val is not None:
            if opt in ['PLUGINS', 'THEMES']:
                val = [ v.strip() for v in val.split(',') ] 
            app.config[opt] = val

def check_options():
    for k, v in REQUIRED_OPTIONS.iteritems():
        if k not in app.config:
            LOGGER.error('%s was not set. Falling back to default: %s', k, v)
            app.config[k] = v

# -------------------
# Building the Logger
# -------------------

logging_setup()

# ------------
# Building app
# ------------

app = Flask('wordpot')
app.url_map.converters['regex'] = RegexConverter

# Import config from file
conffile = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../wordpot.conf')
LOGGER.info('Loading conf file: %s', conffile)
try:
    app.config.from_pyfile(conffile)
except:
    LOGGER.error('Can\'t load conf file')
check_options()

# ----------------------------
# Building the plugins manager
# ----------------------------

pm = PluginsManager()
pm.load()

import wordpot.views
