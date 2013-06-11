"""Handles file uploads."""

import config
import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
from google.appengine.ext.webapp import template
import Datasources.datasource_factory
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    """Listens for uploads, and returns a blob datastore id."""
    
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is the name of the file input field in the form.
        self.response.out.write(config.seshat_home + "/file/" + str(upload_files[0].key()))
        return None
    
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write(unicode(template.render(config.template_path + "test_upload.html", {'upload_url':upload_url})))

class UploadPathHandler(webapp2.RequestHandler):
    """Generates upload paths."""

    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write(upload_url)

def main():
    pass

if __name__ == '__main__':
    main()