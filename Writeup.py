'''
Created on Nov 4, 2015

@author: mjchao
'''

class Writeup( object ):
    
    def __init__( self ):
        
        #figure out what the correct classifications are
        self._correctClassifications = {}
        with open( "test_ground_truth.txt" , "r" ) as f:
            for line in f.readlines():
                if ( not len(line.strip()) == 0 ):
                    pathname , authorName = line.split()
                    
                    filename = pathname[ (pathname.find( "/" )+1) : (pathname.find( "." ))]
                    problemId = filename[ 0 : filename.find( "sample" ) ]
                    docNum = int(filename[ (filename.find( "sample" ) + len( "sample" )) :  ])
                    
                    if ( authorName == "__NONE__" ):
                        authorId = -1
                    else:
                        authorId = int(authorName[ (pathname.find( "Author") + len( "Author")+1) : ])
    
                    self._correctClassifications[ (problemId , docNum) ] = authorId
                    
    
    def print_accuracy( self , documents , classifications ):
        correct = 0
        total = len( documents )
        for i in range(len(documents)):
            doc = documents[ i ]
            if self._correctClassifications[ (doc.get_problem_id() , doc.get_document_num()) ] == classifications[ i ]:
                correct += 1
            else:
                print "Expected:", self._correctClassifications[ (doc.get_problem_id() , classifications[ i ]) ] , "Found:", classifications[ i ]
                
        print "Accuracy:" , 1.0 * correct / total
    
def main():
    test = Writeup()
            
if __name__ == "__main__" : main()