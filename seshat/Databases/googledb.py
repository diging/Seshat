"""Allows Seshat to use the Google App Engine datastore."""

import datetime
import webapp2
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template

def main():
    print "Nothing to see here."

class GPaper(db.Model):
    """The Google datastore model for the Paper object."""
    id = db.StringProperty(required=False)
    uri = db.StringProperty(required=False) 
    
    title = db.StringProperty(required=False)
    journal = db.StringProperty(required=False)
    year = db.StringProperty(required=False)
    
    abstract = db.StringProperty(required=False)
    pdf = db.StringProperty(required=False)
    full_text = db.StringProperty(required=False)
    references_text = db.StringProperty(required=False)
    references = db.ListProperty(basestring)

class GAuthor(db.Model):
    """The Google datastore model for the Author object."""
    pass
    
class GDSpace_Object(db.Model):
    """The Google datastore model for the DSpace_Object object."""
    pass
    
class GCorpus(db.Model):
    """The Google datastore model for the Corpus object."""
    id = db.StringProperty(required=False)
    title = db.StringProperty(required=False)
    papers = db.ListProperty(basestring)
    
class Datastore:
    """This class provides methods for querying data."""
    def __init__(self):
        pass
    
    def search(self, type, field, value):
        """Query the Google Datastore for entities of type type, and return a list of results where field == value."""
        
        type = "G" + type
        results = db.GqlQuery("SELECT * FROM " + type + " WHERE " + field + " = '" + str(value) + "'")
        return results

    def new(self, type):
        """Return a new data entity of the specified type."""
        options = { "Paper": Paper,
                    "Author": Author,
                    "DSpace_Object": DSpace_Object,
                    "Corpus": Corpus
                    }
        def Paper():
            return GPaper()
        def Author():
            return GAuthor()
        def DSpace_Object():
            return GDSpace_Object()
        def Corpus():
            return GCorpus()

if __name__ == '__main__':
    status = main()
    sys.exit(status)