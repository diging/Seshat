"""Gets Papers from a BibTex file."""
import Resources.bib
import logging
import objects
import config

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
            try:    # Resolves issue #25
                paper.title = (self.parser.records[record]['title'], False)
            except KeyError:
                pass
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

            try:
                paper.date = (self.parser.records[record]['issued']['literal'], False)
            except KeyError:
                pass
            
            
            creators = []
            if 'author' in self.parser.records[record]:
                for author in  self.parser.records[record]['author']:
                    try:
                        author_name = author['family'].encode('ascii', 'ignore') + ", " + author['given'].encode('ascii', 'ignore')
                    except KeyError:
                        author_name = author['family'].encode('ascii', 'ignore')

                    matches = objects.Getter().db.retrieve_only('Creator', 'name', author_name)
                    if len(matches) > 0:    # Assume that if we find something, it has to be right.
                        creator = objects.Creator(matches[0])
                    else:   # Should fix #24 !
                        creator = objects.Creator()
                        creator.name = author_name
                        creator.update()
                    creators.append(creator)
          
            paper.creators = ( [ creator.id for creator in creators ], False)
            
            papers.append(paper)
            
        return papers
            
            
def main():
    print "Nothing to see here."

if __name__ == '__main__':
    status = main()
    sys.exit(status)
        
        
        