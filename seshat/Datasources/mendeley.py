"""Connects to Mendeley, and gets Papers from a folder in the user's library."""

import os
import sys


from Resources import mendeley_client
import objects



class data:
    """Methods for getting Papers from a folder in a user's library via the Mendely API."""
    
    def __init__(self):
        """Initialize the connection to the Mendely API. Need to think about how this will work with OAuth."""
        
        self.mendeley = mendeley_client.create_client()  # This will get you started!
        self.FoldersList = []
        
        pass
        
    def list_folders(self):
        """Return a list of folders in a user's Mendeley library."""
        # return a list of folders, probably as tuples: ( title, uri )
        
        FoldersResponse = self.mendeley.folders()
        
        FoldersList = []

        for Folder in FoldersResponse:
            CurrentFolder = {}
            CurrentFolder['Id'] = Folder['id']
            CurrentFolder['Name'] = Folder['name']
            self.FoldersList.insert(len(FoldersList), CurrentFolder)
        #response = mendeley.search('phiC31', items=10)
        return self.FoldersList
        
    def list_papers(self, FolderId):
        """Return a list of all papers in a given folder in a user's Mendeley library. folder should probably be a URI?"""
        
        # return a list of papers, probably as tuples: ( title, uri )
        PapersListInFolder = self.mendeley.folder_documents(FolderId)
        
        # Code to implement paging
        TotalPages = PapersListInFolder['total_pages']
        
        PapersListInFolder = []
        PaperListInPage = []
        
        # Call the function for each page
        for i in range(0, TotalPages):
            PaperListInPage = []
            PapersListInPage = self.mendeley.folder_documents(FolderId,page=i)
            PaperList = PapersListInPage['document_ids']
            for Paper in PaperList:
                PapersListInFolder.insert(len(PapersListInFolder),Paper)
            i = i+1
        
        return PapersListInFolder
        
    def get_paper(self, paper):
        """Return a Seshat Paper object based on the available fields in a given paper. paper should probably be a URI?"""
        
        # return a Seshat Paper object: objects.Paper()

        GivenPaperId = paper
        ResponseFromMendeley = self.mendeley.document_details(GivenPaperId)
        
        #PaperObject = Paper()
                
        return ResponseFromMendeley
        
    def get_pdf(self, paper):
        """Check whether a PDF is available for a given paper, and if so download it and save it to disk."""
        
        # Return the path to the file, or False if no PDF is available.
        
        

    def get_papers(self, folder):
        """Return a list of Seshat Paper objects, given a folder in the user's Mendely library. Each Paper should have as many of the fields filled as possible, and should have a PDF."""
        
        # You probably want to iterate over list_papers(), and for each item do get_paper() and get_pdf().
        
        ListOfPaperIds = self.list_papers(folder)
        
        ListOfPaperObjects = []
        for CurrentPaperId in ListOfPaperIds:
            CurrentPaperResultFromMendeley = self.get_paper(CurrentPaperId)
            CurrentPaperObject = self.getPaperObject(CurrentPaperResultFromMendeley)
            ListOfPaperObjects.insert(len(ListOfPaperObjects),CurrentPaperObject)
        
        return ListOfPaperObjects
        
        # Return a list of Seshat Paper objects.    
    
    def getPaperObject(self, PaperResult):
        """Get the result from get_paper() and return a Paper Seshat object corresponding to the input."""
        CurrentPaper = objects.Paper()
        
        if 'title' in PaperResult.keys():
            CurrentPaper.title = (PaperResult['title'], True)
            
        if 'year' in PaperResult.keys():
            CurrentPaper.date = (PaperResult['year'], True)
            
        if 'abstract' in PaperResult.keys():
            CurrentPaper.abstract = (PaperResult['abstract'], True)
            
        if 'mendeley_url' in PaperResult.keys():
            CurrentPaper.pdf = (PaperResult['mendeley_url'], True)
            
        if 'published_in' in PaperResult.keys():
            CurrentPaper.citation[0]['journal'] = (PaperResult['published_in'], True)
            
        if 'volume' in PaperResult.keys():
            CurrentPaper.citation[0]['volume'] = (PaperResult['volume'], True)
            
        if 'pages' in PaperResult.keys():
            CurrentPaper.citation[0]['pages'] = (PaperResult['pages'], True)
        
        CurrentPaper.source[0]['source'] = ("Mendeley", True)
        
        if 'mendeley_url' in PaperResult.keys():
            CurrentPaper.source[0]['uri'] = (PaperResult['mendeley_url'], True)        

               
        ListOfAuthors = []
        
        if 'authors' in PaperResult.keys():
            for CurrentAuthor in PaperResult['authors']:
                AuthorInstance = CurrentPaper.creators[0][0];
                AuthorInstance['name'] = (CurrentAuthor['surname'] + ', ' + CurrentAuthor['forename'], True)
                ListOfAuthors.insert(len(ListOfAuthors), AuthorInstance)
            CurrentPaper.creators = (ListOfAuthors, True)
        
        return CurrentPaper;
        
        
def main():
    print "Nothing to see here."

if __name__ == '__main__':
    status = main()
    sys.exit(status)