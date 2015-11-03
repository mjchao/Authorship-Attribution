'''
Created on Nov 2, 2015

@author: mjchao
'''

import numpy

'''
Performs author attributions to documents.
'''
class Attributor( object ):
    
    '''
    Creates an Attributor object that will train on the given classified
    documents and attempt to classify the unclassified documents
    '''
    def __init__( self , classifiedDocuments , unclassifiedDocuments , stopwords ):
        self._classified = classifiedDocuments
        self._unclassified = unclassifiedDocuments
        self._stopwords = stopwords
        
        #we'll assume that the number of labels will just be the maximum authorId
        #in our training data
        self._numLabels = max( [ doc.getAuthorId() for doc in classifiedDocuments ] ) + 1
        
      
    '''
    Trains the classifier.
    '''  
    def train( self ):
        authorIds = [ doc.getAuthorId() for doc in self._classified ]
        categoryOccurrences = numpy.array([ 0 for _ in range( 0 , self._numLabels ) ] )
        for authorId in authorIds:
            categoryOccurrences[ authorId ] += 1
         
        #compute P(c)   
        self._categoryProbability = 1.0 * categoryOccurrences / len( self._classified )
        
        #compute number of documents with class label c that contain each stop word
        stopWordOccurrences = numpy.zeros( (len( self._stopwords ) , self._numLabels ) , numpy.int32 )
        for doc in self._classified:
            for i in range( len( self._stopwords ) ):
                if ( doc.containsStopword( self._stopwords[ i ] ) ):
                    stopWordOccurrences[ i ][ doc.getAuthorId() ] += 1
        
        #calculate the probability of a given stop word appearing in a document with a given author
        #using equation 6 in the spec
        self._stopWordProbabilityGivenCategory = (1.0 * stopWordOccurrences + 1) / (numpy.array( [categoryOccurrences] * len(self._stopwords) ) + 2)
        '''Generalized formula
        for i in range( len( self._stopwords ) ):
            for c in range( self._numLabels ):
                stopWordProbabilityGivenCategory[ i ][ c ] = (stopWordOccurrences[ i ][ c ] + 1)/(occurrencesPerCategory[ c ] + self._numLabels)
        ''' 
    
    def classify( self ):
        self._classifications = numpy.array([-1] * len( self._unclassified ))
        for i in range( len(self._unclassified) ):
            
            #decide whether we use P(f|c)) or 1 - P(f|c)
            featureProbability = numpy.array( [ self._stopWordProbabilityGivenCategory[ j ][ : ] if self._unclassified[ i ].containsStopword( self._stopwords[j] ) else \
                                               1.0 - self._stopWordProbabilityGivenCategory[ j ][ : ] \
                                               for j in range(len(self._stopwords)) ] )
            
            #then add those values
            logProbabilitiesSum = numpy.log2( self._categoryProbability ) + numpy.log2(featureProbability)
            labelProbabilities = numpy.sum( logProbabilitiesSum , axis=0 )
            self._classifications[ i ] = numpy.argmax( labelProbabilities ) + 1
    
    def printResults( self ):
        print "Number of authors:" , self._numLabels
        print self._classifications
        pass