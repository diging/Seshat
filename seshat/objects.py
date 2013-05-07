"""Defines the various object types used by seshat."""

import time
import random
import sys
import Databases.factory_provider

db_factory = Databases.factory_provider.get_factory()

# TODO: Create more datastore options.
datastore = "google"

def main():
    print "Nothing to see here."

class SeshatObject:
    """Base class for all data objects used by Seshat. Each new object is given an internal ID, which is based on a unix timestamp."""
    def __init__(self):
        pass

    def start(self):
        """Initialize the SeshatObject."""
        
        
        
        # Link this SeshatObject to a datastore object, e.g. a Google Datastore entity.
        #if self.id is not None:
            # TODO: Check to make sure entity really exists in the datastore.
        #    pass
        #else:
        #    self.id = ds.new(self.__class__.__name__)
            
    def update(self):
        """Updates the database with any new changes to this object."""
        ds.update(self.__class__.__name__, self.id, self)

class Paper(SeshatObject):
    """The Paper is the unit of currency of the whole operation. These are created from data provided by the user or scraped from a web service, and are updated throughout the workflow.
    
    Each property is primarily composed of a 2-tuple, of the form (value, flag). The value can be a string, list, or dictionary. See the variable declarations below to get a sense of the format for each property. 
    
    The flag indicates whether the user has validated the content of the property. Even if the property value was gleaned from a service or data file, the user should manually inspect each field before the object is considered ready for ingestion into the repository."""

    
    def __init__(self, id=None):
        """Create a new paper object. Since different data sources will provide records of varying degrees of completeness, the a new Paper object is initialized without any input.
        
        Call the factory provider to get a database object, with methods load(), update()."""

        self.id = id
        self.title = ("", False)
        self.citation = (
                            {                           # These are the only three fields that we need.
                                'journal': ("", False),
                                'volume': ("", False),
                                'pages': ("", False)
                            }
                        , False)                        # Validation should occur for the citation as a whole.
        self.date = ("", False)                         # This is the year that the paper was published.
        self.description = ("", False)
        self.source = (
                            {
                                'source': ("", False),  # This could be "Mendeley"
                                'uri': ("", False)      # This could be the Mendeley URI
                            }
                        , False)
        self.abstract = ("", False)
        self.creators = ([ 
                            {                           # There should be an object of this format for each author. Validation occurs for each author name and author URI.
                                'name': ("", False),    # The plain-text name, e.g. "Smith, John Q."
                                'uri': ("", False)      # A URI for an entry in an authority file, e.g. http://www.digitalhps.org/concepts/WID-02374451-N-??-horse
                            }
                        ], False)                       # Validation should also occur for the author list as a whole.
        self.pdf = ("", False)               # A path to a PDF.
        self.full_text = ("", False)         # A path to a plain text file.
        self.date_digitized = ("", False)    # http://www.iso.org/iso/iso8601
        self.rights = (
                            {
                                'rights': ("", False),  # A description of the rights
                                'holder': ("", False)   # An entity
                            }
                        , False)
        
        self.references_text = ("", False)   # A path to a plain text file containing bibliographic references.
        self.language = ("eng", False)
        self.type = ("Text", False)

        self.uri = ""                        # This is the handle of the DSpace object, once ingested.

        self.start()
    
    def start(self):
        """Generates a new datastore entity, or loads an existing entity if id is set."""
        
        self.db = db_factory.produce("Paper")
        if self.id is not None:
            self.db.load(id)
            for key, value in self.db.data.iteritems:
                self.__setattr__(key, value)

    def update(self):
        self.db.update(self)

class Author(SeshatObject):
    """An Author refers to a human who wrote something. Each object should refer to a concept in an authority, such as ConceptPower."""
    
    def __init__(self, id=None):
        """Create a new author object. Since working with an author may involve creating new concepts in an authority, the class is initialized without a handle."""

        self.start()
        
        self.name = ""
         
class DSpace_Object(SeshatObject):
    """These are used to prepare papers for ingestion into a DSpace repository. This class is based on the metadata standards for the Digital HPS Community Repository, which is based on Dublin Core."""
    
    def __init__(self, id=None):
        """Create a new dspace object, with the ID of the corresponding paper.
        
        Arguments:
        id -- The ID of the paper (string)."""
        self.id = id        
        self.start()        
    
        # TODO: add metadata fields
        
class Corpus(SeshatObject):
    """A corpus is a collection of papers."""
    
    def __init__(self, id=None, title=""):
        """Create a new corpus. This is basically just a bag of Paper IDs."""
        self.title = title
        self.id = id
        self.start()   

class CorpusEdge(SeshatObject):
    """This is for keeping track of corpora."""
    
    def __init__(self, corpus, paper, id=None):
        """Create a new CorpusEdge."""
        
        self.id = id
        self.Corpus = corpus
        self.Paper = paper
        
        self.start()

if __name__ == '__main__':
    status = main()
    sys.exit(status)