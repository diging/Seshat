"""Human interface for interacting with corpora."""

import config
import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
import Resources.oauth2 as oauth
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template
import Datasources.datasource_factory
import Datasources.mendeley

from google.appengine.api import users

import Databases.factory_provider
datafactory = Databases.factory_provider.get_factory()

class interface:
    """Human interface for interacting with corpora."""

    def __init__(self):
        self.template_values = {
            'seshat_home': config.seshat_home
        }
        return None
    
    def do(self, do, user, request, arg=None):
        """Route actions."""

        #try:
        method = getattr(self, do)
        return method(user, request, arg)
        #except AttributeError:
        #    return "No such method in this class, or downstream error."
    
    def list(self, user, request, id=None):
        """Display a list of all of the corpora."""

        getter = objects.Getter()
        self.template_values['corpora'] = [ objects.Corpus(r) for r in getter.db.retrieve_all("Corpus") ]

        return unicode(template.render(config.template_path + "corpora.html", self.template_values))

    def view(self, user, request, id):
        """Display all of the papers in a corpus."""
        
        corpus = objects.Corpus(id)        
        papers = [ objects.Paper(p) for p in corpus.papers ]
        
        self.template_values['papers'] = [ {
                                                'title': paper.title[0],
                                                'id': paper.id,
                                                'completion': paper.completion()*100,
                                                'data': paper
                                            } for paper in papers]
        self.template_values['corpus_id'] = id
        
        return unicode(template.render(config.template_path + "corpus.html", self.template_values))

    def update(self, user, request, id):
        """Update an existing corpus."""
        pass

    def new(self, user, request, source=None):
        """Provide the interface for creating a new corpus."""
        
        if source is None:
            return unicode(template.render(config.template_path + "add_corpus.html", self.template_values))
        if source == "mendeley":
            return self.new_from_mendeley(user, request)
        else:
            return unicode(template.render(config.template_path + "add_corpus_" + source + ".html", self.template_values))

    def new_from_mendeley(self, user, request, source=None):
        interface = Datasources.mendeley.data()
        response = interface.start(user)
        
        if response is None:
            return "Authenticated."
        else:   # User needs to authorize Seshat to access their account.
            self.template_values['auth_url'] = response
            return unicode(template.render(config.template_path + "mendeley_auth.html", self.template_values))
            
    def authorize_mendeley_post(self, user, request, id=None):
        interface = Datasources.mendeley.data()
        
        verifier = request.get("verification")
        
        if interface.authorize(user, verifier):
            return "Authorized"
            #return self.new_from_mendeley(user, request)
        else:
            return "Oops"
            

    def new_post(self, user, request, id=None):
        """Receive and process a POST request with data to create a new corpus."""

        ds_factory = Datasources.datasource_factory.factory()
        datasource = ds_factory.produce(request.get('datasource'))
        datasource.data(request.get('bibtex'), request.get('title'))
        papers = datasource.get_papers()
        
        corpus = objects.Corpus(None, request.get('title'))
        
        for paper in papers:
            paper.update()
            corpus.papers.append(str(paper.id))
        corpus.update()

        self.template_values['corpus'] =    {
                                                'title': corpus.title,
                                                'id': corpus.id
                                            }

        return unicode(template.render(config.template_path + "add_corpus_success.html", self.template_values))
 
class CorpusHandler(webapp2.RequestHandler):
    """Routes interactions with corpora to the interfaces."""
    
    def get(self, do='list', id=None):
        user = users.get_current_user()
        if user:
            if (do == 'new') and (self.request.get('datasource') != ""):
                arg = self.request.get('datasource')
            else:
                arg = id
        
            response = interface().do(do, user, self.request, arg)
            try:
                self.response.out.write(    unicode(template.render(config.template_path + "head.html", {  'title': do,
                                                                                                    'user_status': user,
                                                                                                    'login': users.create_login_url(self.request.uri),
                                                                                                    'logout': users.create_logout_url('./')
                                                                                                }))
                                        +   response
                                        +   unicode(template.render(config.template_path + "foot.html", {}))
                                        )
            except (TypeError, AttributeError):
                self.response.out.write("No such function.")
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self, do='list', id=None):
        user = users.get_current_user()
        if user:
            #self.response.out.write(unicode(template.render(config.template_path + "head.html", {'title': do})))
            self.response.out.write(interface().do(do + "_post", user, self.request))
            #self.response.out.write(unicode(template.render(config.template_path + "foot.html", {})))
        else:
            self.redirect(users.create_login_url(self.request.uri))

def main():
    pass

if __name__ == '__main__':
    main()