import sys
import main
import Datasources.bibtex as bibtex



def main():
    print 'asdf'

    f = open("test.bib", "rb")
    bib_test = f.read()

    data = bibtex.BibTex_Data(bib_test, "Test")
    data.corpus()

if __name__ == '__main__':
    main()