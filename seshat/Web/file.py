import config

import objects
import os
import urllib2 as urllib
import webapp2
import cgi
import wsgiref.handlers
from google.appengine.ext.webapp import template
import Datasources.datasource_factory
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users

class FileHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """Serves up files from the blobstore, given key."""
    def get(self, key, filename="outfile"):
        key = str(urllib.unquote(key))
        blob_info = blobstore.BlobInfo.get(key)
        self.send_blob(blob_info, save_as=filename)

def main():
    pass

if __name__ == '__main__':
    main()