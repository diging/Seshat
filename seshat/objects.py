"""Defines the various object types used by seshat."""

import time
import random
from Databases.googledb import Datastore
ds = Datastore()


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
        if self.id is not None:
            # TODO: Check to make sure entity really exists in the datastore.
            pass
        else:
            self.id = ds.new(self.__class__.__name__)
            
    def update(self):
        """Updates the database with any new changes to this object."""
        ds.update(self.__class__.__name__, self.id, self)

class Paper(SeshatObject):
    """The Paper is the unit of currency of the whole operation. These are created from data provided by the user, and are updated throughout the workflow."""
    
    def __init__(self, id=None):
        """Create a new paper object.
        
        Since different data sources will provide records of varying degrees of completeness, the class is initialized without any input."""

        self.title = ""
        self.id = id
        self.start()
        
        self.journal = ""
        self.year = ""
        self.abstract = ""
        self.pdf = ""               # A path to a PDF.
        self.full_text = ""         # A path to a plain text file.
        self.references_text = ""   # A path to a plain text file containing bibliographic references.
        self.references = []        # A list of paper IDs.
    
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