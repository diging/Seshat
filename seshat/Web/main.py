import objects
import os
import urllib2
import webapp2
import cgi
import wsgiref.handlers
import config
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template

from google.appengine.api import users


template_path = os.path.join(os.path.dirname(__file__), "templates/")


class RootHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.out.write(    unicode(template.render(template_path + "head.html", {  'seshat_home': config.seshat_home,
                                                                                            'title': 'Hi there!',
                                                                                            'user_status': user,
                                                                                            'login': users.create_login_url(self.request.uri),
                                                                                            'logout': users.create_logout_url('./')
                                                                                        }))
                                +   unicode(template.render(template_path + "main.html", {  'user_status': user,
                                                                                            'login': users.create_login_url(self.request.uri)
                                                                                        }))
                                +   unicode(template.render(template_path + "foot.html", {}))
                                )


def main():
    pass

if __name__ == '__main__':
    main()