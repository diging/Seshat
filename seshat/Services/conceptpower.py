"""Interacts with ConceptPower API to retrieve concept URIs, and (where necessary) add new concepts."""

import requests
import urllib2
import sys

def searchWord(Word, Pos):
    URL = "http://digitalhps-develop.asu.edu:8080/conceptpower/rest/ConceptLookup/"+Word+"/"+Pos+""
    Proxy = "http://digitalhps-develop.asu.edu:8080" 
    Data = urllib2.urlopen(URL).read()    
    print Data
    
def main():
    print "Nothing to see here."
    searchWord("Mike", "noun")

if __name__ == '__main__':
    status = main()
    sys.exit(status)
    
    
