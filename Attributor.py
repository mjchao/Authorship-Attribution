'''
Created on Nov 2, 2015

@author: mjchao
'''

class Attributor( object ):
    
    def __init__( self , classifiedDocuments , unclassifiedDocuments ):
        self._classified = classifiedDocuments
        self._unclassified = unclassifiedDocuments