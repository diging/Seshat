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

        return client.folders()
        
    def list_papers(self, FolderId):
        """Return a list of all papers in a given folder in a user's Mendeley library."""
        
        PapersListInFolder = client.folder_documents(FolderId)
        
        # Code to implement paging
        TotalPages = PapersListInFolder['total_pages']
        
        PapersListInFolder = []
        PaperListInPage = []
        
        # Call the function for each page
        for i in range(0, TotalPages):
            PaperListInPage = []
            PapersListInPage = client.folder_documents(FolderId,page=i)
            PaperList = PapersListInPage['document_ids']
            for Paper in PaperList:
                PapersListInFolder.insert(len(PapersListInFolder),Paper)
            i = i+1
        
        return PapersListInFolder
        
    def get_paper(self, paper):
        return client.document_details(paper)
        
    def get_pdf(self, paper):
        """Check whether a PDF is available for a given paper, and if so download it and save it to disk."""
    
        paper_details = self.get_paper(paper)

        try:
            pdf = client.download_file(paper, paper_details['files'][0]['file_hash'])
            blob = objects.db_factory.produce("Blob")   # For storing the pdf
            key = blob.write(pdf['data'], "application/pdf")
            return config.seshat_home + "/file/" + str(key)
        except IndexError:
            return None

    def get_papers(self, folder):
        """Return a list of Seshat Paper objects, given a folder in the user's Mendely library. Each Paper should have as many of the fields filled as possible, and should have a PDF."""
                
        ListOfPaperIds = self.list_papers(folder)
        
        ListOfPaperObjects = []
        for CurrentPaperId in ListOfPaperIds:
            CurrentPaperResultFromMendeley = self.get_paper(CurrentPaperId)
            CurrentPaperObject = self.getPaperObject(CurrentPaperResultFromMendeley)
            ListOfPaperObjects.append(CurrentPaperObject)
        
        return ListOfPaperObjects
        
        # Return a list of Seshat Paper objects.    
    
    def getPaperObject(self, PaperResult):
        """Get the result from get_paper() and return a Paper Seshat object corresponding to the input."""
        
        CurrentPaper = objects.Paper()
        
        try: CurrentPaper.title = (PaperResult['title'], True)
        except KeyError: pass
        try: CurrentPaper.date = (PaperResult['year'], True)
        except KeyError: pass
        try: CurrentPaper.abstract = (PaperResult['abstract'], True)
        except KeyError: pass
        
        pdf_url = self.get_pdf(PaperResult['id'])
        if pdf_url is not None:
            CurrentPaper.pdf = (pdf_url, True)
        else:
            CurrentPaper.pdf = ("", False)
        
        try: CurrentPaper.citation[0]['journal'] = (PaperResult['published_in'], True)
        except KeyError: pass
        try: CurrentPaper.citation[0]['volume'] = (PaperResult['volume'], True)
        except KeyError: pass
        try: CurrentPaper.citation[0]['pages'] = (PaperResult['pages'], True)
        except KeyError: pass

        
        CurrentPaper.source[0]['source'] = ("Mendeley", True)
        
        try: CurrentPaper.source[0]['uri'] = (PaperResult['mendeley_url'], True)
        except KeyError: pass
        
        CurrentPaper.creators = ([], False)
        try:
            for CurrentAuthor in PaperResult['authors']:
                CurrentPaper.creators[0].append({
                                                    'name': (CurrentAuthor['surname'] + ', ' + CurrentAuthor['forename'], False),
                                                    'uri': ('', False)
                                                })
        except KeyError: pass

        return CurrentPaper
        
def main():
    print "Nothing to see here."

if __name__ == '__main__':
    status = main()
    sys.exit(status)