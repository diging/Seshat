# Seshat metadata management system for HPS

## Dependencies

This is designed to run on Google App Engine, but attempts are being made to make it as separable as possible (e.g. abstracting away from the GAE datastore). You'll need the following libraries, which will need to be installed (at least symlinks) in the main Seshat/ directory:

* [networkx](http://networkx.github.io/)
* [httplib2](https://code.google.com/p/httplib2/)
* [requests](http://docs.python-requests.org/en/latest/)