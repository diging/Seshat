import os
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(100)

template_path = os.path.join(os.path.dirname(__file__), "Web/templates/")
seshat_home = "http://localhost:8080"
seshat_root = os.path.dirname(__file__)

licenses = [
                "Closed",
                "Another license",
                "A third license"
            ]