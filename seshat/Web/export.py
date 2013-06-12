import objects
from google.appengine.api import urlfetch
import config
import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
import logging
from google.appengine.api import users
import cStringIO as StringIO
import Databases
db_factory = Databases.factory_provider.get_factory()


from contextlib import closing
from zipfile import ZipFile, ZIP_STORED

class ExportHandler(webapp2.RequestHandler):
    
    def get(self, corpus_id):
        # Check whether user is logged in.
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            
        
        corpus = objects.Corpus(corpus_id)
        if corpus is not None:
            
            papers = [ objects.Paper(p) for p in corpus.papers ]

            # Initialize the zip file.
            outfile = StringIO.StringIO()
            outzip = ZipFile(file=outfile, mode='w')

            # Write CSV file, and add to zip.
            csv_file = ""
            
            # Max number of creators?
            creators = 0
            for paper in papers:
                if len(paper.creators[0]) > creators:
                    creators = len(paper.creators[0])
            
            headers = 'Filename,Title,Date,Description Abstract,Description,Source,Source Uri,Date Digitized,Type,Language,Relation Ispartof,Rights,Rights Holder'
            for i in range(0, creators):
                headers += ',Creator,Creator Uri'
            csv_file += headers + '\n'
            
            for paper in papers:
                if paper.pdf[0] != '':  # Fixes issue #31
                    line = str(paper.id) + ".pdf|" + str(paper.id) + "-cocr.txt|" + str(paper.id) + "-references.txt"
                    line += ',"' + paper.title[0] + '"'
                    line += ',' + paper.date[0]
                    line += ',"' + paper.abstract[0].replace("\"", "") + '"'
                    line += ',"' + paper.citation[0]['journal'][0] + ' ' + paper.citation[0]['volume'][0] + ': ' + paper.citation[0]['pages'][0] + '"'
                    line += ',"' + paper.source[0]['source'][0] + '"'
                    line += ',' + str(paper.source[0]['uri'][0])
                    line += ',' + paper.date_digitized[0]
                    line += ',"' + paper.type[0] + '"'
                    line += ',' + paper.language[0]
                    line += ',http://hdl.handle.net/10776/3984'
                    line += ',"' + paper.rights[0]['rights'][0] + '"'
                    line += ',"' + paper.rights[0]['holder'][0] + '"'
                    
                    for id in paper.creators[0]:
                        creator = objects.Creator(id)
                        line += ',"' + creator.name + '"'
                        line += ',' + str(creator.uri)
                    
                    csv_file +=  line + '\n'
            outzip.writestr(str(corpus_id) + ".csv", csv_file, compress_type=ZIP_STORED)
                
            # Write files to zip, and send to blobstore.

            for paper in papers:
                if paper.pdf[0] != '':  # Fixes issue #31
                    logging.error(paper.pdf[0])
                    
                    outzip.writestr(str(paper.id) + ".pdf", urlfetch.fetch(paper.pdf[0]).content,  compress_type=ZIP_STORED)
                    outzip.writestr(str(paper.id) + "-cocr.txt", urlfetch.fetch(paper.full_text[0]).content,  compress_type=ZIP_STORED)
                    
                    if paper.references_text[0] != '':  # Fixes issue #30
                        outzip.writestr(str(paper.id) + "-references.txt", urlfetch.fetch(paper.references_text[0]).content,  compress_type=ZIP_STORED)

            outzip.close()
            outfile.seek(0)
            
            blob = db_factory.produce("Blob")
            key = blob.write(outfile.getvalue(), 'application/zip')
            self.redirect(config.seshat_home + "/file/" + str(key))