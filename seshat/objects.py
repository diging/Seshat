"""Defines the various object types used by seshat."""

import time
import random
import sys
import Databases.factory_provider
import logging
from pprint import pprint

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
        """Generates a new datastore entity, or loads an existing entity if id is set."""
        
        logging.debug("Initializing a SeshatObject of type " + self.__class__.__name__)
        self.db = db_factory.produce(self.__class__.__name__)
        if self.id is not None:
            logging.debug("Loading SeshatObject of type " + self.__class__.__name__ + ", with id " + str(self.id))
            if self.db.load(self.id):
                for key, value in self.db.data.iteritems():
                    setattr(self, key, value)
            else:
                logging.debug("objects.py: failed to load SeshatObject of type " + self.__class__.__name__ + ", with id " + str(self.id))
                self.id = None
        return None

    def update(self):
        """Calls the update() method of the db entity."""
        
        logging.debug("Updating SeshatObject of type " + self.__class__.__name__ + ", with id " + str(self.id))
        self.id = self.db.update(self)
        return self.id

    def completion(self):
        """Checks how many of the attributes have been validated, and returns the proportion (float)."""

        attributes = 0.0
        validated = 0.0
        for key, value in self.__dict__.iteritems():
            try:    # Only want attributes that are tuples, since those are the ones that can be validated.
                if value[1]: validated += 1
                attributes += 1
            except (AttributeError, IndexError):
                pass
        return validated/attributes
    
    def delete(self):   # Issues #29 and #37
        """Calls the delete method for the db entity associated with the SeshatObject."""
        
        logging.debug("Deleting SeshatObject of type " + self.__class__.__name__ + ", with id " + str(self.id))
        
        if self.db is not None:
            self.db.delete()
        return None


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
        
        self.creators = ([], False)             # A list of IDs for Creator objects.
        
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
        self.language = ("eng", True)
        self.type = ("Text", True)

        self.uri = ""                        # This is the handle of the DSpace object, once ingested.

        self.start()


class DSpace_Object(SeshatObject):
    """These are used to prepare papers for ingestion into a DSpace repository. This class is based on the metadata standards for the Digital HPS Community Repository, which is based on Dublin Core."""
    
    def __init__(self, id=None):
        """Create a new dspace object, with the ID of the corresponding paper.
        
        Arguments:
        id -- The ID of the paper (string)."""
        self.id = id        
        self.start()        
    
        # TODO: add metadata fields

class Creator(SeshatObject):
    def __init__(self, id=None, name=None, uri=None):
        self.id = id
        self.name = name        # The plain-text name, e.g. "Smith, John Q."
        self.uri = uri          # A URI for an entry in an authority file, e.g. http://www.digitalhps.org/concepts/WID-02374451-N-??-horse
        self.start()

class Corpus(SeshatObject):
    """A corpus is a collection of papers."""
    
    def __init__(self, id=None, title=""):
        """Create a new corpus. This is basically just a bag of Paper IDs."""

        self.id = id
        self.title = title
        self.papers = []
        self.start()

class Getter(SeshatObject):
    """A class for grabbing bunches of things."""

    def __init__(self):
        self.id = None
        self.start()

class Token(SeshatObject):
    """A class for storing tokens."""

    def __init__(self, id=None):
        self.id = id
        
        self.start()

class Generic(SeshatObject):
    """A Generic object."""
    
    def __init__(self, generic_id=None):
        self.id = None
        self.generic_key = None
        self.value = None
        self.start()

class CorpusEdge(SeshatObject):
    """This is for keeping track of corpora."""
    
    def __init__(self, corpus, paper, id=None):
        """Create a new CorpusEdge."""
        
        self.id = id
        self.Corpus = corpus
        self.Paper = paper
        
        self.start()
        
class AuthorMap(SeshatObject):
    
    def __init__(self, id=None):
    
        self.id = id
        self.name = None    # The authoritative name of this author (should be LoC format, or thereabouts).
        self.strings = []   # Strings that have corresponded to this author.
        self.start()

if __name__ == '__main__':
    status = main()
    sys.exit(status)