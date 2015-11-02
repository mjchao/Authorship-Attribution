'''
Created on Nov 2, 2015

@author: mjchao
'''

import sys
import os
from Document import Document , DocumentType

def run():
    pass

def createDocuments( directory  ):
    filenames = next(os.walk( directory ))[2]
    trainDocs = []
    sampleDocs = []
    for filename in filenames:
        newDocument = Document.createDocument( directory , filename )
        if ( newDocument.getDocumentType() == DocumentType.SAMPLE ):
            sampleDocs.append( newDocument )
        elif ( newDocument.getDocumentType() == DocumentType.TRAIN ):
            trainDocs.append( newDocument )
        else:
            print "An error occurred while parsing document " + directory + filename
            
    return [ trainDocs , sampleDocs ]
    

def main():
    documentList = createDocuments( sys.argv[ 1 ] )
    trainDocs = documentList[ 0 ]
    sampleDocs = documentList[ 1 ]
    
    print "Found" , len( trainDocs ) , "training documents and" , len( sampleDocs ) , "sample documents"
    print "Training Documents:"
    for doc in trainDocs:
        print doc
        
    print ""
    print "Sample Documents:"
    for doc in sampleDocs:
        print doc
    
    pass


if __name__ == "__main__" : main()