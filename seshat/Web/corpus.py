"""Human interface for interacting with corpora."""

import config
import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
import Resources.oauth2 as oauth
from google.appengine.ext.webapp import template
import Datasources.datasource_factory
import Datasources.mendeley
import itertools

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

    def new(self, user, request, source=None):
        """Provide the interface for creating a new corpus."""
        
        if source is None:
            return unicode(template.render(config.template_path + "add_corpus.html", self.template_values))
        if source == "mendeley":
            return self.new_from_mendeley(user, request)
        else:
            return unicode(template.render(config.template_path + "add_corpus_" + source + ".html", self.template_values))

    def new_from_mendeley(self, user, request, source=None):
        """If a user has already authorized Seshat to access the Mendeley library, will access their account and list folders to choose from. Otherwise, will direct user to an authorization page."""
        
        interface = Datasources.mendeley.data()
        response = interface.start(user.user_id())    # If there is no key for this user, will return an auth_url and generic_key for a request token.
        
        if response is None:
            
            if request.get('folder'):   # User has selected a folder. Prompt to proceed.
                if request.get('proceed'):  # User has confirmed creation of corpus from folder. Create new corpus.
                    papers = interface.list_papers(request.get('folder'))   # List of Mendeley paper IDs
                    folder = [ f for f in interface.list_folders() if f['id'] == request.get('folder') ][0]     # Get the name of the folder.
                
                    corpus = objects.Corpus(None, folder['name'])
                    corpus.update()
                    
                    template_file = "add_corpus_mendeley_do.html"
                    self.template_values['papers'] = papers
                    self.template_values['folder'] = request.get('folder')
                    self.template_values['corpus'] = corpus.id
    
                else:   # User has not confirmed creation of corpus from folder.
                    self.template_values['folder_id'] = request.get('folder')
                    template_file = "add_corpus_mendeley_folders_prompt.html"

            else:   # User has not selected a folder. Display a list of folders to choose from.
                self.template_values['folders'] = interface.list_folders()
                template_file = "add_corpus_mendeley_folders.html"
    
        else:   # User needs to authorize Seshat to access their account.
            self.template_values['auth_url'] = response[0]
            self.template_values['request_token_key'] = response[1]
            template_file = "mendeley_auth.html"
            
        return unicode(template.render(config.template_path + template_file, self.template_values))
    
    def creators (self, user, request, id=None):
        """Provides an interface to correct and validate authors across the entire corpus."""
        
        corpus = objects.Corpus(id)        
        papers = [ objects.Paper(p) for p in corpus.papers ]
        
        creator_ids = []
        for paper in papers:
            for id in paper.creators[0]:
                if id not in creator_ids:
                    creator_ids.append(id)
        creators = [ objects.Creator(id) for id in creator_ids ]
#        return str(creators)

        self.template_values['creators'] = [    {
                                                    'id': creator.id,
                                                    'name': creator.name,
                                                    'uri': creator.uri
                                                } for creator in creators ]
        self.template_values['papers'] = papers
                                                
        return unicode(template.render(config.template_path + "creators.html", self.template_values))
                
        
    
    def new_paper_from_mendeley_post(self, user, request, id=None):
        """Receives a Mendeley paper id, creates a new Paper, and returns its ID. If not ID given, returns None."""
        
        interface = Datasources.mendeley.data()
        response = interface.start(user.user_id())
        
        id = request.get("id")
        if id is not None:
            paper = interface.getPaperObject(interface.get_paper(id))
            paper.update()
            
            return '{ "title": "'+ paper.title[0] +'", "pdf_url": "' + paper.pdf[0] + '", "id": "' + str(paper.id) + '" }'
        return None
            
    def update_post(self, user, request, id=None):
        """Receives a Corpus id and instructions to add or remove a paper (given requests.get("do") and requests.get("id")), and returns true. If no id given, returns false."""
        
        id = request.get("id")
        if id is not None:
            corpus = objects.Corpus(id)
            paper = request.get("paper")
            if request.get("do") == "add":  # Don't want duplicate entries.
                corpus.papers.append(paper)
            elif request.get("do") == "remove":
                try: corpus.papers.remove(paper)
                except Error: pass  # Paper may not be in corpus.
            corpus.update()
            return True
        return None
            
    def authorize_mendeley_post(self, user, request, id=None):
        """Receives authorization requests from the authorization page, and returns result."""
        
        interface = Datasources.mendeley.data()
        
        verifier = request.get("verification")
        request_token_key = request.get("request_token_key")
        
        if interface.authorize(user.user_id(), verifier, request_token_key):
            return "success"
        else:
            return "fail"
            
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
        
    def delete_post(self, user, request, id=None):  # Issue #37
        """Deletes a corpus and all of its papers."""

        id = request.get("id")
        if id is not None:
            corpus = objects.Corpus(id)
            
            for paper in corpus.papers:
                objects.Paper(paper).delete()
            
            return corpus.delete()        
            return None
        return "No ID provided."
 
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
            #try:
            self.response.out.write(    unicode(template.render(config.template_path + "head.html", {  'title': do,
                                                                                                'user_status': user,
                                                                                                'login': users.create_login_url(self.request.uri),
                                                                                                'logout': users.create_logout_url('./')
                                                                                            }))
                                    +   response
                                    +   unicode(template.render(config.template_path + "foot.html", {}))
                                    )
            
            #except (TypeError, AttributeError):
               # self.response.out.write("No such function.")
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