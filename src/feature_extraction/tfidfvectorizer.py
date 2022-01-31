from collections import Counter
import os
from matplotlib.pyplot import axis
import numpy as np


'''
TfidfVectorizer is a class that following methods:
    1. label:
        - It basically labels the documents of which category it is. 
        - gives dictionary named label_dict
        - dictionary has values as: {'dir_name':[start_index,end_index]}
    
    2. vocabulary:
        - method that returns a dictionary.
        - dictionary has values as: {'word':[count,index]}

    3. documentTermMat:
        - It gives 2D numpy array that corresponds to document-term matrix where each document represent unique rows and each term represent unique column.
        - also indexes the word.
'''
class TfidfVectorizer():
    def __init__(self):
        # input_list is the list of unique words.
        self.input_list = []

        # vocab is the dictionary that contains the count and index of unique words in a document.
        self.vocab = {}

        # vec is the numpy array of document term matrix.
        self.vec = None

        # result is the numpy array that contains tfidf vector.
        self.result = None

        # label_dict is the dictionary that index a document 
        self.label_dict = {}


    def label(self, root = '.\\preprocessed_test_data\\'):
        
        # root = '.\\16NepaliNews\\raw\\'
        # root = '.\\preprocessed_test_data\\'

        # list of directory
        dirs = os.listdir(root)

        # initializing a dictionary with keys as directories in root folder and values as None.
        self.label_dict = dict.fromkeys(dirs,None)

        start = 1

        for dir in dirs:
            #number of files in a dir
            file_count= len(os.listdir(os.path.join(root,dir)))
            
            self.label_dict[dir] = [start,file_count+start-1]
            start+=file_count


    def vocabulary(self, input_list, vocab)-> dict:

        self.input_list = input_list
        self.vocab = vocab
        x=[]

        for word in self.input_list:

            if word in self.vocab:
                #increasing count of word
                self.vocab[word][0]+=1
            else:
                x=[1,0]
                self.vocab[word] = x
                
        return self.vocab
    
    def documentTermMat(self, Path=".\\preprocessed_test_data", input_text=''):
        # initializing empty dictionary for unique words in the documents
        self.vocab = {}

        mat = []

        # when path is given
        if Path and not input_text:  
            root = Path
            # list of dirs inside root
            dirs = [os.path.join(root, path) for path in os.listdir(root)]
            
            for i in range(len(dirs)):  # [education,health,sports,.....]
                
                # if directory
                if os.path.isdir(dirs[i]):  

                    for filename in os.listdir(dirs[i]):

                        with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:

                            # list of an article
                            text = (fp.read()).split() 

                            #calling vocabulary method by passing text (list of words) and vocab as parameter. 
                            self.vocab = self.vocabulary(text,self.vocab)

                # if not directory
                else:  

                    with open(dirs[i], encoding='utf-8') as fp:

                        # list of an article
                        text = (fp.read()).split()

                        #calling vocabulary method by passing text (list of words) and vocab as parameter.
                        self.vocab = self.vocabulary(text,self.vocab)

            #list of unique words
            wordlist=list(self.vocab.keys())
            

            for i in range(len(dirs)):

                # if directory
                if os.path.isdir(dirs[i]):

                    # no. of filename(documents)=no. of columns
                    for filename in os.listdir(dirs[i]):
                        row = []  # initializing first row
                        with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:

                            #list of an article
                            text = (fp.read()).split()
                            #initializing counter
                            cnt = Counter(text)
                            
                            for x in range(len(wordlist)):

                                # adding index of word in vocab dictionary
                                self.vocab[wordlist[x]][1]=x

                                if wordlist[x] in text:
                                    row.append(cnt[wordlist[x]])
                                else:
                                    row.append(0)
                        mat.append(row)

        # numpy array of document-term matrix
        self.vec=np.array(mat)
    
    
    def tf_idf(self):
        '''
            term-frequency (tf) =   (Number of repeatition of words in document)
                                    --------------------------------------------
                                         (Number of words in a document)

            inverse-document-frequency (idf) =              (Number of document)
                                                ------------------------------------------
                                                    (Number of document containing words)

            tf-idf = tf * idf
        '''
        tf= self.vec/self.vec.sum(axis=1)[:,np.newaxis]

        idf=np.log(self.vec.shape[0]/np.count_nonzero(self.vec,axis=0))

        self.result=tf*idf
        

obj = TfidfVectorizer()
obj.documentTermMat()
obj.tf_idf()
obj.label()
print(obj.vocab)
print('.'*100)
print(obj.vec)
print('.'*100)
print(obj.result)
print('.'*100)
print(obj.label_dict)







