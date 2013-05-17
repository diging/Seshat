"""Connects to Mendeley, and gets Papers from a folder in the user's library."""

import os
import sys
import config
from Resources import mendeley_client
import Resources.oauth2 as oauth
import objects
import time


import Databases.factory_provider
datafactory = Databases.factory_provider.get_factory()

config_file = config.seshat_root + "/Resources/mendeley_config.json"
keys_file = config.seshat_root + "/Resources/keys_api.mendeley.com.pkl"

mendeley_config = mendeley_client.MendeleyClientConfig(config_file)

host = 'api.mendeley.com'
if hasattr(mendeley_config, "host"):
    host = mendeley_config.host

client = mendeley_client.MendeleyClient(mendeley_config.api_key, mendeley_config.api_secret, {"host":host})
tokens_store = mendeley_client.MendeleyTokensStore()


class data:
    """Methods for getting Papers from a folder in a user's library via the Mendely API."""
    
    def __init__(self):
        """Initialize the connection to the Mendely API. Need to think about how this will work with OAuth."""
        self.FoldersList = []
        
        return None
        
    def start(self, user_id):
        """If the user has already authorized Seshat to access their Mendeley library, then set access token and return None. Otherwise, pass back an auth_url for the user to visit."""
        
        access_token = tokens_store.get_access_token(user_id)
        
        if not access_token:    # User needs to authorize Seshat to access their Mendeley account.
            request_token, auth_url = client.get_auth_url()

            request_token_store = datafactory.produce("Generic")    # Will need the request_token later, to finish the authorization.
            request_token_store.generic_key = str(user_id + str(int(time.time())))
            request_token_store.value = str(request_token)
            request_token_store.update(request_token_store)
            return auth_url, request_token_store.generic_key
        else:
            client.set_access_token(access_token)
        return None
    
    def authorize(self, user_id, verifier, request_token_key):
        """Connects to Mendeley with request token and verifier (provided by user). If successful, adds a new authorization key to the token store and returns true. Otherwise, returns false."""
        
        request_token_store = datafactory.produce("Generic")
        
        request_token_store.load(request_token_key)
        request_token = oauth.Token.from_string(str(request_token_store.value))
        try:
            client.set_access_token(client.verify_auth(request_token, verifier))
            tokens_store.add_account(user_id,client.get_access_token())
            tokens_store.save()
            return True
        except Exception:   # If client.verify_auth() fails, throws a ValueError "Invalid parameter string."
            return False
    
    def list_folders(self):
        """Return a list of folders in a user's Mendeley library."""
        
        FoldersResponse = client.folders()
        
        FoldersList = []

        for Folder in FoldersResponse:
            CurrentFolder = {}
            CurrentFolder['Id'] = Folder['id']
            CurrentFolder['Name'] = Folder['name']
            self.FoldersList.insert(len(FoldersList), CurrentFolder)

        return self.FoldersList
        
    def list_papers(self, FolderId):
        """Return a list of all papers in a given folder in a user's Mendeley library. folder should probably be a URI?"""
        
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
        

        ResponseFromMendeley = self.mendeley.document_details(paper)
        
        #PaperObject = Paper()
                
        return ResponseFromMendeley
        
    def get_pdf(self, paper):
        """Check whether a PDF is available for a given paper, and if so download it and save it to disk."""
        
        # Return the path to the file, or False if no PDF is available.
        
        

    def get_papers(self, folder):
        """Return a list of Seshat Paper objects, given a folder in the user's Mendely library. Each Paper should have as many of the fields filled as possible, and should have a PDF."""
                
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