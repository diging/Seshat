"""Seshat uses a variety of graphs to keep track of bibliographic relationships."""

import networkx

def main():
    print "Nothing to see here."
    
class author_papers (networkx.Graph):
    """This graph describes relationships between authors and their papers."""
    
    def __init__(self, meta):
        """Creates a new networkx graph object.
        
        Arguments:
        meta --  An account of how the data were generated (dict)."""
        
        self.graph['meta'] = meta
        
    def add(author, paper, year):
        """Creates new nodes for author and paper, if they don't already exist. Then adds an edge connecting them, with a year attribute.
        
        Arguments:
        author -- An author ID (string).
        paper -- A paper ID (string).
        year -- A four-digit publication year (int).
        
        Returns True if added successfully."""
        
        # TODO: check whether nodes exist for author and paper in self.graph, and if not create new nodes.
        # TODO: check whether edge exists connecting author and paper (with same pub year) in self.graph, and if not create new edge.
        return None
        
class co_authors (networkx.Graph):
    """This graph describes relationships between co-authors."""
    
    def __init__(self, meta):
        """Creates a new networkx graph object.
        
        Arguments:
        meta --  An account of how the data were generated (dict)."""
        
        self.graph['meta'] = meta
        
    def add(author_one, author_two, paper, year):
        """Creates new nodes for authors, if they don't already exist. Then adds an edge connecting them, with paper ID and year attributes.
        
        Arguments:
        author_one -- An author ID (string).
        author_two -- Another author ID (string).
        paper -- A paper ID (string).
        year -- A four-digit publication year (int).
        
        Returns True if added successfully."""
        
        # TODO: check whether nodes exist for authors in self.graph, and if not create new nodes.
        # TODO: check whether edge exists connecting authors (with same paper ID) in self.graph, and if not create new edge.
        return None

class bibliographic_couplings(networkx.Graph):
    """This graph describes bibliographic couplings between papers."""
    
    def __init__(self, meta):
        """Creates a new networkx graph object.
        
        Arguments:
        meta --  An account of how the data were generated (dict)."""
        
        self.graph['meta'] = meta

class citations(networkx.Graph):
    """This graph describes direct citations between papers."""
    
    def __init__(self, meta):
        """Creates a new networkx graph object.
        
        Arguments:
        meta --  An account of how the data were generated (dict)."""
        
        self.graph['meta'] = meta
        
class co_citations(networkx.Graph):
    """This graph describes co-citations between papers."""
    
    def __init__(self, meta):
        """Creates a new networkx graph object.
        
        Arguments:
        meta --  An account of how the data were generated (dict)."""

        self.graph['meta'] = meta


if __name__ == '__main__':
    status = main()
    sys.exit(status)