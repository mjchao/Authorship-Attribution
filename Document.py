'''
Created on Nov 2, 2015

@author: mjchao
'''

class Document( object ):
    
    def __init__( self , authorId , text ):
        self._authorId = authorId
        self._text = text
        self._tokens = Document.tokenize( text )
        
    @staticmethod
    def createDocument( filename ):
        pass
    
    @staticmethod
    def tokenize( text ):
        pass
    
    
'''
Unit testing
'''
def main():
    pass

if __name__ == "__main__" : main()