"""Creates a new Corpus (with Papers and Authors) from a BibTex file."""

import bib
import Seshat.objects

class BibTex_Data:
    def __init__(self, data, title):
    """Use [BibPy][] to parse BibTex input.
    
        [bibpy]: https://github.com/ptigas/bibpy
    
    Arguments:
    data -- BibTex data (str)."""
    
        self.title = title
        self.parser = bib.Bibparser(data)
        self.parser.parse()
        
    def corpus(self)
        """Generates a new Corpus. Checks each record in the BibTex file: if a Paper already exists, then get its ID. Otherwise, create a new paper. Adds Paper ids to Corpus.papers."""
        
        corpus = Seshat.objects.Corpus(None, self.title)

        for record in self.parser.records:
            found = false
            # TODO: search for Paper, and get paper_id
            if found:
                corpus.papers.append(paper_id)
            else:
                # TODO create new papers
                pass
                
        
        
        