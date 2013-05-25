"""Interacts with ConceptPower API to retrieve concept URIs, and (where necessary) add new concepts."""

import requests
import urllib2
import sys
import xml.etree.ElementTree as ET

vowels = ['a', 'e', 'i', 'o', 'u', 'y']

class authority:

    def __init__(self):
        self.server = "http://chps.asu.edu/conceptpower/rest/"
        
    def search (self, query):
        """Searches for word of type pos, and returns a list of tuples: (result, uri)."""
        
        query = query.replace(" ", "%20")
#        sys.exit(query)
        response = urllib2.urlopen(self.server+"ConceptLookup/"+query+"/Noun").read()
        root = ET.fromstring(response)
        if len(root) > 0:
            return [ (elem[1].text, elem[0].text) for elem in root ]
        return []

    def suggest(self, word):
        """Conducts a series of searches based on manipulations of word, and returns a list of word-uri suggestions."""

        suggestions = []
        word_split = word.split(",")

        if len(word_split) > 1:     # Maybe of form: Last, First M.
            suggestions += self.search(word_split[1] + " " + word_split[0])
            suggestions += self.search(word_split[0])
        else:
            suggestions += self.search(word)  # Try at face-value.
        
        return suggestions

def main():
    
    print suggest("Bradshaw, Anthony")

if __name__ == '__main__':
    status = main()
    sys.exit(status)
    
    
