"""Gets Papers from a BibTex file."""
import Resources.bib
import objects

class data:
    """Methods for converting a BibTex data file into a list of Seshat Paper objects."""
        
    def data(self, data, title):
        """Use [BibPy][] to parse BibTex data.
    
            [bibpy]: https://github.com/ptigas/bibpy
        
        Arguments:
        data -- BibTex data (str)."""
    
        self.title = title
        self.parser = Resources.bib.Bibparser(data)
        self.parser.parse()
        
    def get_papers(self):
        """Returns a list of Seshat Paper objects."""
        
        papers = []
                
        for record in self.parser.records:
            paper = objects.Paper()
            paper.title = (self.parser.records[record]['title'], False)
            try:
                paper.citation[0]['journal'] = (self.parser.records[record]['journal'], False)
            except KeyError:
                pass
                
            try:
                paper.citation[0]['volume'] = (self.parser.records[record]['volume'], False)
            except KeyError:
                pass
                
            try:
                paper.citation[0]['pages'] = (self.parser.records[record]['pages'], False)
            except KeyError:
                pass

            paper.date = (self.parser.records[record]['issued']['literal'], False)
            
            authors = []
            for author in  self.parser.records[record]['author']:
                try:
                    authors.append( {
                                        'name': (author['family'].encode('ascii', 'ignore') + ", " + author['given'], False),
                                        'uri': ("", False)
                                    })
                except KeyError:
                    authors.append(author['family'])            
            paper.creators = (authors, False)                        
            
            papers.append(paper)
            
        return papers
            
            
def main():
    print "Nothing to see here."

if __name__ == '__main__':
    status = main()
    sys.exit(status)
        
        
        