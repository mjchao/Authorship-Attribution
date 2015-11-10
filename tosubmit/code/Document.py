'''
Created on Nov 2, 2015

@author: mjchao
'''

import re
import string

class DocumentType:
    SAMPLE_STR = "sample"
    TRAIN_STR = "train"
    
    SAMPLE = 0
    TRAIN = 1
    
    '''
    Determines the document type of a file - it is either "sample"
    or "train" and receives an ID 0 or 1, respectively.
    '''
    @staticmethod
    def get_document_type( filename ):
        if ( DocumentType.SAMPLE_STR in filename ):
            return DocumentType.SAMPLE
        elif ( DocumentType.TRAIN_STR in filename ):
            return DocumentType.TRAIN
        
    '''
    Converts a document type ID to a string. If the ID is 0, then
    "sample" will be returned, and if the ID is 1, then "train"
    will be returned. Otherwise, "?" will be returned if the ID
    is not known.
    '''
    @staticmethod
    def convertTypeToString( documentType ):
        if ( documentType == DocumentType.SAMPLE ):
            return DocumentType.SAMPLE_STR
        elif ( documentType == DocumentType.TRAIN ):
            return DocumentType.TRAIN_STR
        
        return "?"

'''
Represents a word document.
'''
class Document( object ):
    
    '''
    Creates a document object 
    '''
    def __init__( self , problemId , documentType , documentNumber , authorId , text ):
        self._problemId = problemId
        self._docType = documentType
        self._docNum = documentNumber
        self._authorId = authorId
        self._text = text
        self._tokens = Document.tokenize( text )
       
    '''
    Returns a document object that represents the text document
    with the associated directory and filename
    ''' 
    @staticmethod
    def createDocument( directory , fileWithExtension ):
        
        #remove the extension from the file to get the filename
        filename = fileWithExtension[ 0 : fileWithExtension.find( "." ) ]
        problemId = filename[ 0 ]
        documentType = DocumentType.get_document_type( filename )
        
        documentNumber = -1
        authorId = -1
        
        #sample documents do not have an authorId
        if ( documentType == DocumentType.SAMPLE ):
            startOfNum = filename.find( DocumentType.SAMPLE_STR ) + len( DocumentType.SAMPLE_STR )
            endOfNum = len( filename )
            documentNumber = int( filename[ startOfNum : endOfNum ] )
            
        #training documents have author IDs followed by numbers
        elif ( documentType == DocumentType.TRAIN ):
            startOfAuthorId = filename.find( DocumentType.TRAIN_STR ) + len( DocumentType.TRAIN_STR )
            endOfAuthorId = filename.find( "-" ) 
            authorId = int( filename[ startOfAuthorId : endOfAuthorId ] )
            
            startOfDocumentNum = filename.find( "-" ) + 1
            endOfDocumentNum = len( filename )
            documentNumber = int( filename[ startOfDocumentNum : endOfDocumentNum ] )
        
        with open( directory + fileWithExtension , "r" ) as f:
            content = f.read()

        return Document( problemId , documentType , documentNumber , authorId , content )

    '''
    Removes leading, trailing, and extra spaces from a string
    '''
    @staticmethod
    def remove_extra_space( input_string ):
        return re.sub("\s+", " ", input_string.strip())
    
    '''
    Converts some text into a list of tokens
    '''
    @staticmethod
    def tokenize( text ):
        extra_space_removed = Document.remove_extra_space( text )
        punctuation_removed = "".join([x for x in extra_space_removed if x not in string.punctuation])
        lowercased = punctuation_removed.lower()
        return lowercased.split()
    
    def get_document_type( self ):
        return self._docType
    
    def get_document_num(self):
        return self._docNum
    
    def get_problem_id(self):
        return self._problemId
    '''
    Returns the ID of this author minus 1. We subtract 1 so that
    we can still have 0-indexed arrays.
    '''
    def get_author_id( self ):
        return self._authorId-1
    
    def contains_stopword( self , stopword ):
        return stopword in self._tokens
    
    '''
    Reports the textual representation of this document for debugging purposes. 
    Only the first 10 tokens of the text will be shown to limit output size.
    '''
    def __str__( self ):
        initialText = ""
        for i in range( 0 , min(10 , len(self._tokens)) ):
            initialText += self._tokens[ i ] + " "
            
        if ( len( self._tokens ) > 10 ):
            initialText = "{" + initialText.strip() + " ... }"
        else :
            initialText = "{" + initialText.strip() + "}"
            
        return "Document[ ProblemId=" + str( self._problemId ) + \
            " , DocumentType=" + DocumentType.convertTypeToString( self._docType ) + \
            " , DocumentNumber=" + str( self._docNum ) + \
            " , AuthorId=" + str( self._authorId ) + \
            " , Text=" + str( initialText ) +\
            " ]" 
    
    
'''
Unit testing
'''
def main():
    doc1 = Document.createDocument( "problemset/problemA/" , "Asample02.txt" )
    print doc1
    
    doc2 = Document.createDocument( "problemset/problemA/" , "Atrain01-1.txt" )
    print doc2
    
    doc3 = Document.createDocument( "problemset/problemA/" , "Atrain03-3.txt" )
    print doc3
    
    doc4 = Document.createDocument( "problemset/problemB/" , "Bsample13.txt" )
    print doc4
    
    doc5 = Document.createDocument( "problemset/problemM/" , "Msample10.txt" )
    print doc5

if __name__ == "__main__" : main()