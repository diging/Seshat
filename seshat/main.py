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
import Web.services
import Web.export

import wsgiref.handlers

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
        webapp2.Route(r'/file/<key>/<filename>', handler=Web.file.FileHandler),

        webapp2.Route(r'/service/conceptpower/<word>', handler=Web.services.ConceptPowerHandler),
        
        webapp2.Route(r'/upload', handler=Web.uploads.UploadHandler),
        webapp2.Route(r'/upload_path', handler=Web.uploads.UploadPathHandler),

        webapp2.Route(r'/favicon.ico', handler=Web.null.NullHandler),
        webapp2.Route(r'/export/<corpus_id>', handler=Web.export.ExportHandler)
    ])
    
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
