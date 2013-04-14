"""Creates a new Corpus (with Papers and Authors) from a BibTex file."""

import bib
import objects
from pprint import pprint

class BibTex_Data:
    def __init__(self, data, title):
        """Use [BibPy][] to parse BibTex input.
    
            [bibpy]: https://github.com/ptigas/bibpy
        
        Arguments:
        data -- BibTex data (str)."""
    
        self.title = title
        self.parser = bib.Bibparser(data)
        self.parser.parse()
        
    def corpus(self):
        """Generates a new Corpus. Creates a new Paper for each record, and creates new CorpusEdges."""
        
        corpus = objects.Corpus(None, self.title)
        papers = []
        edges = []
        
        for record in self.parser.records:
            paper = objects.Paper()
            paper.title = self.parser.records[record]['title']
            try:
                paper.journal = self.parser.records[record]['journal']
            except KeyError:
                pass
            paper.year = self.parser.records[record]['issued']['literal']
            paper.update()
            papers.append(paper)
            
            edge = objects.CorpusEdge(corpus.id, paper.id)
            edge.update()
            
            
            
def main():
    print "Nothing to see here."

if __name__ == '__main__':
    status = main()
    sys.exit(status)
        
        
        