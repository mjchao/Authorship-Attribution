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
        self._numLabels = max( [ doc.get_author_id() for doc in classifiedDocuments ] ) + 1
        
      
    '''
    Trains the classifier.
    '''  
    def train( self ):
        
        #compute N_c, the number of documents provided for each author
        authorIds = [ doc.get_author_id() for doc in self._classified ]
        categoryOccurrences = numpy.array([ 0 for _ in range( 0 , self._numLabels ) ] )
        for authorId in authorIds:
            categoryOccurrences[ authorId ] += 1
         
        #compute P(c), the prior probability that any random document is
        #written by each author   
        self._categoryProbability = 1.0 * categoryOccurrences / len( self._classified )
        
        #compute N_ci, the number of documents with class label c that contain each stop word
        stopWordOccurrences = numpy.zeros( (len( self._stopwords ) , self._numLabels ) , numpy.int32 )
        for doc in self._classified:
            for i in range( len( self._stopwords ) ):
                if ( doc.contains_stopword( self._stopwords[ i ] ) ):
                    stopWordOccurrences[ i ][ doc.get_author_id() ] += 1
        
        #calculate the probability of a given stop word appearing in a document with a given author
        #using equation 6 in the spec
        self._stopWordProbabilityGivenCategory = (1.0 * stopWordOccurrences + 1) / (numpy.array( [categoryOccurrences] * len(self._stopwords) ) + 2)
    
    '''
    Looks at all the unclassified documents and tries to determine the author
    that wrote the document 
    '''
    def classify( self ):
        self._classifications = numpy.array([-1] * len( self._unclassified ))
        
        #classify every document
        for i in range( len(self._unclassified) ):
            
            #Determine the probability of each feature occurring.
            #Each feature is either the occurrence or the non-occurrence
            #of the stop word. 
            #
            #If the feature is the occurrence of the stop word
            #(i.e. the stop word appears in the document), then the probability
            #of that feature is the posterior probability that the stop word
            #appearing in the document given its author: P(f|c).
            #
            #If the feature is the non-occurrence of the stop word
            #(i.e. the stop word does not appear in the document), then the
            #probability of that feature is the posterior probability that the
            #stop word does not appear in the document given its author: 1 - P(f|c)
            self._featureProbabilityGivenCategory = numpy.array( [ (self._stopWordProbabilityGivenCategory[ j ][ : ]) if self._unclassified[ i ].contains_stopword( self._stopwords[j] ) \
                                                        else (1.0 - self._stopWordProbabilityGivenCategory[ j ][ : ]) \
                                                        for j in range(len(self._stopwords)) ] )
            
            #Then multiply together the posterior probabilities of seeing each feature given
            #each category. This product is the likelihood that the given author is the true
            #author of the document.
            #s
            #Since the calculation might underflow, we instead add up the logs of those
            #probabilities instead. 
            labelScore = numpy.sum( numpy.log2(self._categoryProbability) + numpy.log2(self._featureProbabilityGivenCategory) , axis=0 )
            
            #We declare the most likely author of the document. 
            #This is done by taking the argmax over the probabilities 
            #of each author being the true author of the document.
            self._classifications[ i ] = numpy.argmax( labelScore ) + 1
    
    def get_results( self ):
        return self._classifications
    
    def get_feature_ranking( self ):
        classConditionalEntropy = -1.0 * numpy.sum( self._categoryProbability * self._featureProbabilityGivenCategory * numpy.log( self._featureProbabilityGivenCategory ) , axis=1)
        rankings = []
        for i in range(len(classConditionalEntropy)):
            rankings.append( (self._stopwords[ i ] , classConditionalEntropy[ i ]) )
            
        rankings.sort( cmp=lambda x,y: 1 if x[1] < y[1] else -1 )
        return rankings
    
    def get_feature_frequencies( self ):
        frequencies = []
        for word in self._stopwords:
            count = 0
            for doc in self._classified:
                if ( doc.contains_stopword( word )):
                    count += 1
                
            frequencies.append(1.0 * count / len( self._classified ))
            
        rankings = []
        for i in range( len(frequencies) ):
            rankings.append( (self._stopwords[ i ] , frequencies[ i ]) )
            
        rankings.sort( cmp=lambda x,y: 1 if x[1]<y[1] else -1 )
        return rankings
        