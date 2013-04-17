"""Connects to Mendeley, and gets Papers from a folder in the user's library."""

from Resources.mendeley_client import *

class data:
    """Methods for getting Papers from a folder in a user's library via the Mendely API."""
    
    def __init__(self):
        """Initialize the connection to the Mendely API. Need to think about how this will work with OAuth."""

        mendeley = create_client()  # This will get you started!
        
        pass
        
    def list_folders(self):
        """Return a list of folders in a user's Mendeley library."""
        
        # return a list of folders, probably as tuples: ( title, uri )
        
    def list_papers(self, folder):
        """Return a list of all papers in a given folder in a user's Mendeley library. folder should probably be a URI?"""
        
        # return a list of papers, probably as tuples: ( title, uri )
                
    def get_paper(self, paper):
        """Return a Seshat Paper object based on the available fields in a given paper. paper should probably be a URI?"""
        
        # return a Seshat Paper object: objects.Paper()
        
    def get_pdf(self, paper):
        """Check whether a PDF is available for a given paper, and if so download it and save it to disk."""
        
        # Return the path to the file, or False if no PDF is available.

    def get_papers(self, folder):
        """Return a list of Seshat Paper objects, given a folder in the user's Mendely library. Each Paper should have as many of the fields filled as possible, and should have a PDF."""
        
        # You probably want to iterate over list_papers(), and for each item do get_paper() and get_pdf().
        
        # Return a list of Seshat Paper objects.    

def main():
    print "Nothing to see here."

if __name__ == '__main__':
    status = main()
    sys.exit(status)