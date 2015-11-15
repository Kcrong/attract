#!/usr/bin/python

import sys
sys.path.insert(0, '/var/www/sunrindcon')

activate_this = '/var/www/sunrindcon/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


from app import app as application
