"""Human interface for interacting with papers."""

import config
import logging
import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
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
        """Receives asynchronous requests from the paper view interface, so that changes to a paper can be stored as they are made.
        
        request should have the following values:
            - field
            - validated
            - value
        """
        
        paper = objects.Paper(id)
        path = request.get('field').split(".")
        validated = bool(request.get('validated'))
        value = request.get('value')
            
        logging.error(path)
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
        
    def update_creator_post (self, request, id):
        action = request.get("action")      # Can be 'add', 'update', 'remove'
        creator_id = request.get("id")              # ID for a creator object
        creator_name = request.get("name")
        creator_uri = request.get("uri")
        
        
        if creator_id != '': creator_id = int(creator_id)
        else: creator_id = None
        
        if creator_name == "": creator_name = "New"
        
        # Load Paper if ID is provided.
        paper_id = int(request.get("paper"))        
        if paper_id != 0: paper = objects.Paper(paper_id)   
        
        if action == 'add':
            if creator_id is not None:    # ID is provided...
                logging.error("ID provided, loading Creator object: " + str(creator_id))
                creator = objects.Creator(creator_id)
            else:   # ID is not provided. Check whether a creator object already exists...
                logging.error("ID not provided. Checking for existing Creator with name: " + creator_name)
                matches = objects.Getter().db.retrieve_only('Creator', 'name', creator_name)
                if (len(matches) > 0) and (creator_name != "New"): 
                    logging.error("Creator with matching name found: " + creator_name)
                    creator = objects.Creator(matches[0])
                else:
                    logging.error("No matching Creator found; generate new Creator: " + creator_name)
                    creator = None
            if creator is None:     # No matching creator found. Create one from scratch...
                logging.error("Generating new Creator.")
                creator = objects.Creator()
                creator.name = creator_name
                creator.uri = creator_uri
                creator.update()
            
            if paper_id != 0:   # We may just want to create a new Creator, and not assign it to a Paper.
                if creator.id not in paper.creators[0]:
                    paper.creators[0].append(creator.id)
                    paper.update()
            return creator.id
            
        if action =='update':
            creator = objects.Creator(creator_id)
            creator.name = creator_name
            creator.uri = creator_uri
            creator.update()
            return creator.id
        
        if action =='remove':   # Should remove from paper, but leave creator entity intact.
            while creator_id in paper.creators[0]:
                paper.creators[0].remove(creator_id)
            paper.update()
            
        if action == 'load':    # Retrieve a Creator based on its ID.
            if creator_id is not None:
                return objects.Creator(creator_id).name
            else:
                return None
            
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
                if do == 'update':
                    self.response.out.write(interface().update_post(self.request, id))
                if do == 'update_creator':
                    self.response.out.write(interface().update_creator_post(self.request, id))
        else:
            self.redirect(users.create_login_url(self.request.uri))

def main():
    pass

if __name__ == '__main__':
    main()