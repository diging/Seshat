import objects
import graphs
import sys
import objects
import urllib2
import webapp2
import cgi
from google.appengine.ext.webapp import template
import Web.corpus
import Web.paper
import Web.null
import Web.main
import Web.uploads
import Web.file

import wsgiref.handlers
from google.appengine.dist import use_library
use_library('django', '1.2')

def main():
    app = webapp2.WSGIApplication([
        webapp2.Route(r'/', handler=Web.main.RootHandler),

        webapp2.Route(r'/corpus', handler=Web.corpus.CorpusHandler),
        webapp2.Route(r'/corpus/<do>', handler=Web.corpus.CorpusHandler),
        webapp2.Route(r'/corpus/<do>/<id>', handler=Web.corpus.CorpusHandler),

        webapp2.Route(r'/paper', handler=Web.paper.PaperHandler),
        webapp2.Route(r'/paper/<id>', handler=Web.paper.PaperHandler),
        webapp2.Route(r'/paper/<id>/<do>', handler=Web.paper.PaperHandler),
        
        webapp2.Route(r'/file/<key>', handler=Web.file.FileHandler),
        
        webapp2.Route(r'/upload', handler=Web.uploads.UploadHandler),
        webapp2.Route(r'/upload_path', handler=Web.uploads.UploadPathHandler),

        webapp2.Route(r'/favicon.ico', handler=Web.null.NullHandler)
    ])
    
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
