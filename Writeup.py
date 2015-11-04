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

        print "Accuracy:" , 1.0 * correct / total
        
    def print_confusion_matrix( self , documents , classifications ):
        actual = []
        for doc in documents:
            actual.append( self._correctClassifications[ (doc.get_problem_id() , doc.get_document_num()) ] )
            
        Writeup.printConfMat( actual , classifications )
        
        
    ## Function to print the confusion matrix.
    ## Argument 1: "actual" is a list of integer class labels, one for each test example.
    ## Argument 2: "predicted" is a list of integer class labels, one for each test example.
    ## "actual" is the list of actual (ground truth) labels.
    ## "predicted" is the list of labels predicted by your classifier.
    ## "actual" and "predicted" MUST be in one-to-one correspondence.
    ## That is, actual[i] and predicted[i] stand for testfile[i].
    @staticmethod
    def printConfMat( actual , predicted):
        complete_list = actual[:]
        complete_list.extend( predicted )
        all_labels = sorted(set(complete_list))
        assert(len(actual) == len(predicted))
        confmat = {}  ## Confusion Matrix
        for i,a in enumerate(actual): confmat[(a, predicted[i])] = confmat.get((a, predicted[i]), 0) + 1
        print
        print
        print "0",  ## Actual labels column (aka first column)
        for label2 in all_labels:
            print label2,
        print
        for label in all_labels:
            print label,
            for label2 in all_labels:
                print confmat.get((label, label2), 0),
            print
    
def main():
    test = Writeup()
            
if __name__ == "__main__" : main()