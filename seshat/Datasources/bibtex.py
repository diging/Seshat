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
        
    def corpus(self):
        """Generates a new Corpus. Checks each record in the BibTex file: if a Paper already exists, then gets its ID. Otherwise, creates a new paper. Adds Paper ids to Corpus.papers."""
        
        corpus = Seshat.objects.Corpus(None, self.title)

        #for record in self.parser.records:
            # Must share title, at least one author, and publication year to be considered a match.
        #    matches = ds.search("Paper", "title", record.title)
        #    if len(matches) > 0:
        #        for match in matches:
        #            if match.year == record.year && match.
           
        #    if found:
        #        corpus.papers.append(paper_id)
        #    else:
                # TODO create new papers
        #        pass
                
        
        
        