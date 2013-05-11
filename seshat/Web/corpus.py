"""Human interface for interacting with corpora."""

import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template

template_path = os.path.join(os.path.dirname(__file__), "templates/")

class interface:
    """Human interface for interacting with corpora."""

    def __init__(self):
        return None
    
    def do(self, do, request, arg=None):
        """Route actions."""

        try:
            method = getattr(self, do)
            return method(request, arg)
        except AttributeError:
            return "No such method in this class, or downstream error."
    
    def list(self, request, id=None):
        """Display a list of all of the corpora."""

        getter = objects.Getter()
        corpora = [ objects.Corpus(r) for r in getter.db.retrieve_all("Corpus") ]
        
        return unicode(template.render(template_path + "corpora.html", { 'corpora': corpora }))

    def view(self, request, id):
        """Display all of the papers in a corpus."""
        
        values = {}
        corpus = objects.Corpus(id)
        for key, value in corpus.db.data.iteritems():
            values[key] = value
        
        return unicode(template.render(template_path + "corpus.html", values))

    def update(self, request, id):
        """Update an existing corpus."""
        pass

    def new(self, request, source=None):
        """Create a new corpus."""
        
        if source is None:
            return unicode(template.render(template_path + "add_corpus.html", {}))
        else:
            return unicode(template.render(template_path + "add_corpus_" + source + ".html", {}))

    def new_post(self, request, source):
        return request.get('bibtex')

class CorpusHandler(webapp2.RequestHandler):
    """Routes interactions with corpora to the interfaces."""
    
    def get(self, do='list', id=None):
        if (do == 'new') and (self.request.get('datasource') != ""):
            arg = self.request.get('datasource')
        else:
            arg = id
        
        try:
            self.response.out.write(unicode(template.render(template_path + "head.html", {'title': do}))
                                +   interface().do(do, self.request, arg)
                                +   unicode(template.render(template_path + "foot.html", {}))
            )
        except (TypeError, AttributeError):
            self.response.out.write("No such function.")

    def post(self, do='list', id=None):
        self.response.out.write(unicode(template.render(template_path + "head.html", {'title': do})))
        if (do == 'new') and (self.request.get('datasource') is not None):
            self.response.out.write(interface().do(do + "_post", self.request, self.request.get('datasource')))
        self.response.out.write(unicode(template.render(template_path + "foot.html", {})))

def main():
    pass

if __name__ == '__main__':
    main()