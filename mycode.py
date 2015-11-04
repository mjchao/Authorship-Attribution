'''
Created on Nov 2, 2015

@author: mjchao
'''

import sys
import os
import matplotlib.pyplot as plt
from Document import Document , DocumentType
from Attributor import Attributor
from Writeup import Writeup

'''
Creates Document objects to represent all the documents in a given
directory that are named properly.

@param directory - the directory in which the document files are.
                    this MUST end with a "/"
'''
def createDocuments( directory  ):
    filenames = next(os.walk( directory ))[2]
    trainDocs = []
    sampleDocs = []
    for filename in filenames:
        newDocument = Document.createDocument( directory , filename )
        try:
            if ( newDocument.get_document_type() == DocumentType.SAMPLE ):
                sampleDocs.append( newDocument )
            elif ( newDocument.get_document_type() == DocumentType.TRAIN ):
                trainDocs.append( newDocument )
            else:
                print "The following document could not be parsed: " + directory + filename
        except:
            print "The following document could not be parsed: " + directory + filename
            
    return [ trainDocs , sampleDocs ]
    
'''
Runs the Bayesian classifier
'''
def main():
    
    #read in training documents and documents to classify
    documentList = createDocuments( sys.argv[ 1 ] )
    trainDocs = documentList[ 0 ]
    sampleDocs = documentList[ 1 ]
        
    #read in stopwords
    with open( "stopwords.txt" , "r" ) as f:
        stopwords = Document.tokenize( f.read() )
    
    #classify the documents with missing authors
    attributor = Attributor( trainDocs , sampleDocs , stopwords )
    attributor.train()
    attributor.classify()
    
    writeup = Writeup()
    results = attributor.get_results()
    writeup.print_accuracy( sampleDocs , results )
    
    writeup.print_confusion_matrix( sampleDocs , results )
    
    print
    print
    featureRankings = attributor.get_feature_ranking()
    print "Feature ranking:"
    for i in range( 0 , 20 ):
        print featureRankings[ i ][ 0 ] , featureRankings[ i ][ 1 ]
    
    print 
    print
    featureFrequencies = attributor.get_feature_frequencies()
    featurePlotDataX = []
    featurePlotDataY = []
    for numFeatures in range(10,len(featureFrequencies)+1,10):
        newStopwords = [ featureFrequencies[ i ][ 0 ] for i in range( 0 , numFeatures ) ]
        newAttributor = Attributor( trainDocs , sampleDocs , newStopwords )
        newAttributor.train()
        newAttributor.classify()
        newResults = newAttributor.get_results()
        accuracy = writeup.get_accuracy( sampleDocs , newResults )
        featurePlotDataX.append( numFeatures )
        featurePlotDataY.append( accuracy )
        
    print "Feature curve:"
    for i in range(len(featurePlotDataX)):
        print featurePlotDataX[ i ] , featurePlotDataY[ i ]
        
    plt.plot( featurePlotDataX , featurePlotDataY )
    plt.xlabel( "Number of Features" )
    plt.ylabel( "Accuracy" )
    plt.title( "Accuracy vs. Number of Features" )
    plt.show()
    
    
    
    


if __name__ == "__main__" : main()