"""Allows Seshat to use the Google App Engine datastore."""

import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Paper(db.Model):
    id = db.StringProperty(required=True)
    uri = db.StringProperty(required=False) 
    
    title = db.StringProperty(required=False)
    journal = db.StringProperty(required=False)
    year = db.StringProperty(required=False)
    
    abstract = db.StringProperty(required=False)
    pdf = db.StringProperty(required=False)
    full_text = db.StringProperty(required=False)
    references_text = db.StringProperty(required=False)
    references = db.ListProperty(basestring)

class Author(db.Model):

class DSpace_Object(db.Model):

class Corpus(db.Model):



