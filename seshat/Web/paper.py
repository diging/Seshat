"""Human interface for interacting with papers."""

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

template_path = os.path.join(os.path.dirname(__file__), "templates/")

class interface:
    """Human interface for interacting with papers."""

    def __init__(self):
        self.template_values = {
            'seshat_home': 'http://localhost:9080'
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
        return "You're crazy."

    def view (self, request, id):
        self.template_values['paper'] = objects.Paper(id)
        return unicode(template.render(template_path + "paper_.html", self.template_values))

    def update (self, request, id):
        pass


class PaperHandler(webapp2.RequestHandler):
    """Routes interactions with papers to the interface."""

    def get(self, do='view', id=None):
        user = users.get_current_user()
        if user:
            arg = id
            try:
                self.response.out.write(unicode(template.render(template_path + "head.html", {'title': do}))
                                    +   interface().do(do, self.request, arg)
                                    +   unicode(template.render(template_path + "foot.html", {}))
                )
            except (TypeError, AttributeError):
                self.response.out.write("No such function.")
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self, do='view', id=None):
        user = users.get_current_user()
        if user:
            if id is not None:
                paper = objects.Paper(id)
                path = self.request.get('field').split(".")
                validated = bool(self.request.get('validated'))
                value = self.request.get('value')
                
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
        else:
            self.redirect(users.create_login_url(self.request.uri))
    

def main():
    pass

if __name__ == '__main__':
    main()