"""Human interface for interacting with papers."""

import config
import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template
import Datasources.datasource_factory

from google.appengine.api import users

class interface:
    """Human interface for interacting with papers."""

    def __init__(self):
        self.template_values = {
            'seshat_home': config.seshat_home
        }
        return None

    def do(self, do, request, arg=None):
        """Route actions."""

        #try:
        method = getattr(self, do)
        return method(request, arg)
        #except AttributeError:
        #    return "No such method in this class, or downstream error."

    def list (self, request, arg):
        """Not sure why this is here."""
        
        return "You're crazy."

    def view (self, request, id):
        """Provides an editing interface for the user."""
        
        self.template_values['paper'] = objects.Paper(id)
        self.template_values['corpus_id'] = request.get('corpus')
        self.template_values['licenses'] = config.licenses
        
        return unicode(template.render(config.template_path + "paper_.html", self.template_values))

    def update_post (self, request, id):
        """Receives asynchronous requests from the paper view interface, so that changes to a paper are stored as they are made."""
        
        paper = objects.Paper(id)
        path = request.get('field').split(".")
        validated = bool(request.get('validated'))
        value = request.get('value')
        
        # User sets a value that has no parent.
        if len(path) == 1:  
            setattr(paper, path[0], (value.replace("\n", ""), validated))
    
        # User indicates that a field is correct.
        elif path[-1] == 'validated':
        
            # The field has no parent.
            if len(path) == 2:
                field_value = getattr(paper, path[0])[0]
                setattr(paper, path[0], (field_value, validated))
            
            # The field has a parent.
            if len(path) > 2:
                field_value = paper.__dict__[str(path[0])][0][str(path[1])][0]
                paper.__dict__[str(path[0])][0][str(path[1])] = (field_value, validated)
    
        # User sets a value for a nested field.
        elif len(path) > 1:
            paper.__dict__[str(path[0])][0][str(path[1])] = (value, validated)
        paper.update()

        return None


class PaperHandler(webapp2.RequestHandler):
    """Routes interactions with papers to the interface."""

    def get(self, do='view', id=None):
        """Routes GET requests."""
        
        user = users.get_current_user()
        if user:
            arg = id
            response = interface().do(do, self.request, arg)
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

    def post(self, do='view', id=None):
        """Routes POST requests."""
        
        user = users.get_current_user()
        if user:
            if id is not None:
                self.response.out.write(interface().update_post(self.request, id))
        else:
            self.redirect(users.create_login_url(self.request.uri))

def main():
    pass

if __name__ == '__main__':
    main()