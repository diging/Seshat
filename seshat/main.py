import objects
import graphs
import sys
import objects

def main():
    paper = objects.Paper()
    paper.title = ("Test!", True)
    
    corpus = objects.Corpus()
    corpus.title = "This is a test corpus."
    corpus.papers = ["1","2","3"]
    corpus.update()
    print "Nothing to see here."

if __name__ == '__main__':
    main()
