import logging
import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
import config
import json
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template

from google.appengine.api import users
import Services.conceptpower

class ConceptPowerHandler(webapp2.RequestHandler):
    """Gets word, responds with JSON-formatted suggestions."""
    
    def get(self, word):
        cp = Services.conceptpower.authority()
        response = [ { 'name': suggestion[0], 'uri': suggestion[1] } for suggestion in cp.suggest(word) ]
        self.response.out.write(json.dumps(response))
        
def main():
    pass

if __name__ == '__main__':
    main()
        