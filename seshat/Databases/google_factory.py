"""Allows Seshat to use the Google App Engine datastore."""

import datetime
import webapp2
import pickle
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template

class factory:
    """A factory that produces database-linked objects."""
    
    def produce(type):
        if type == "Paper":
            return GooglePaper()
            
class GooglePaper:
    """A Paper object that maps Papers onto Google Datastore entities."""
    
    def __init__():
        """Do nothing."""
        pass
        
    def load(self, id):
        """Get a Google Datastore paper_entity, and map Paper fields onto Google Datastore paper entity."""
        pass
    
    def update(self):
        """Map Paper fields onto Google Datastore paper entity, and put it."""
        
        
class paper_entity(db.Model):
    """The Google datastore model for the Paper object."""
    uri = db.StringProperty(required=False) 
        
    title = db.StringProperty(required=False)
    title_validated = db.BooleanProperty(required=False)
        
    journal = db.StringProperty(required=False)
    journal_validated = db.BooleanProperty(required=False)
    
    volume = db.StringProperty(required=False)
    volume_validated = db.BooleanProperty(required=False)

    pages = db.StringProperty(required=False)
    pages_validated = db.BooleanProperty(required=False)

    citation_validated = db.BooleanProperty(required=False)

    date = db.StringProperty(required=False)
    date_validated = db.BooleanProperty(required=False)
        
    description = db.StringProperty(required=False)
    description_validated = db.BooleanProperty(required=False)

    source = db.StringProperty(required=False)
    source_validated = db.BooleanProperty(required=False)

    source_uri = db.StringProperty(required=False)
    source_uri_validated = db.BooleanProperty(required=False)        

    abstract_uri = db.StringProperty(required=False)
    abstract_uri_validated = db.BooleanProperty(required=False) 
    
    creators_list = db.ListProperty(basestring)
    creators_list_validated = db.ListProperty(bool)
    creators_uri_list = db.ListProperty(basestring)
    creators_uri_list_validated = db.ListProperty(bool)
    creators_validated = db.BooleanProperty(required=False)
    
    pdf = db.StringProperty(required=False)
    pdf_validated = db.BooleanProperty(required=False)       

    full_text = db.StringProperty(required=False)
    full_text_validated = db.BooleanProperty(required=False)               
    
    date_digitized = db.StringProperty(required=False)
    date_digitized_validated = db.BooleanProperty(required=False)       

    rights = db.StringProperty(required=False)
    rights_validated = db.BooleanProperty(required=False)       
    
    references_text = db.StringProperty(required=False)
    references_text_validated = db.BooleanProperty(required=False)       

    language = db.StringProperty(required=False)
    language_validated = db.BooleanProperty(required=False)    

    type = db.StringProperty(required=False)
    type_validated = db.BooleanProperty(required=False) 
        

class GAuthor(db.Model):
    """The Google datastore model for the Author object."""
    pass
    
class GDSpace_Object(db.Model):
    """The Google datastore model for the DSpace_Object object."""
    pass
    
class GCorpus(db.Model):
    """The Google datastore model for the Corpus object."""
    title = db.StringProperty(required=False)

class GCorpusEdge(db.Model):
    """The Google datastore model for the CorpusEdge object."""
    Corpus = db.ReferenceProperty(GCorpus)
    Paper = db.ReferenceProperty(GPaper)

class GSeshatGraph(db.Model):
    """The Google datastore model for the SeshatGraph object."""
    title = db.StringProperty(required=False)
    type = db.StringProperty(required=False)
    pickle = db.BlobProperty(required=False)
    
class Datastore:
    """This class provides methods for querying data."""
    def __init__(self):
        pass
    
    def search(self, type, field, value):
        """Query the Google Datastore for entities of type type, and return a list of results where field == value."""
        
        type = "G" + str(type)
        results = db.GqlQuery("SELECT * FROM " + type + " WHERE " + field + " = '" + str(value) + "'")
        return results

    def new(self, type):
        """Returns ID of new data entity of the specified type."""

        if type == "Paper":
            entity = GPaper()
        if type == "Author":
            entity = GAuthor()
        if type == "DSpace_Object":
            entity = GDSpace_Object()
        if type == "Corpus":
            entity = GCorpus()
        if type == "CorpusEdge":
            entity = GCorpusEdge()
        if type == "SeshatGraph":
            entity = GSeshatGraph()
            
        entity.put()
        return entity.key().id()
    
    def load(self, type, id):
        """Retrieve a data entity of specified type and id from the datstore, and return it."""
        key = db.Key.from_path(type, id)
        return db.get(key)
        
    def update(self, type, id, object):
        """Updates a data entity of type and id, using data from object."""
        type = "G" + type
        key = db.Key.from_path(type, id)
        entity = db.get(key)

        if type == "GPaper":
            entity.title = object.title
            entity.journal = object.journal
            entity.year = object.year
            entity.abstract = object.abstract
            entity.pdf = object.pdf
            entity.full_text = object.full_text
            entity.references_text = object.references_text
            entity.references = object.references         
        if type == "GAuthor":
            pass
        if type == "GDSpace_Object":
            pass
        if type == "GCorpus":
            entity.title = object.title
        if type == "GCorpusEdge":
            entity.Corpus = db.get(db.Key.from_path("GCorpus", object.Corpus)) 
            entity.Paper = db.get(db.Key.from_path("GPaper", object.Paper))
        if type == "GSeshatGraph":
            entity.title = object.title
            entity.type = object.__class__.__name__
            entity.pickle = pickle.dump(object)
            
        entity.put()

def main():
    print "Nothing to see here."
    
if __name__ == '__main__':
    status = main()
    sys.exit(status)