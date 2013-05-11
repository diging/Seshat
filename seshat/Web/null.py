"""Does nothing."""

import urllib2
import webapp2
import cgi
import wsgiref.handlers

class NullHandler(webapp2.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()