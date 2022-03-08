from collections import Counter
import os
from matplotlib.pyplot import axis
import numpy as np



class TfidfVectorizer():
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


    def label(self, root = '.\\Preprocessed\\'):

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


    def vocabulary(self,  input_list="",  path="")-> dict:
        if path != "":
            with open(path, "r", encoding="utf-8" ) as fp:
                text = fp.read()
            self.input_list = text.split()
        else:
            self.input_list = input_list

        x=[]

        for word in self.input_list:

            if word in self.vocab:
                #increasing count of word
                self.vocab[word][0]+=1
            else:
                x=[1,0]
                self.vocab[word] = x



    def documentTermMat(self, Path=".\\Preprocessed", input_text=''):
        # initializing empty dictionary for unique words in the documents
        self.vocab = {}

        mat = []

        # when path is given
        if Path and not input_text:
            root = Path
            # list of dirs inside root
            dirs = [os.path.join(root, path) for path in os.listdir(root)]
            # print(dirs)
            fol= len(dirs)
            for i in range(fol):  # [education,health,sports,.....]
                print(dirs[i])
                # if directory
                # print(f"{i} of {fol} {dirs[i]}                     ", end="\r")
                if os.path.isdir(dirs[i]):
                    files = os.listdir(dirs[i])
                    print(files[0], len(files))
                    for filename in files:
                        print(filename)
                        with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:

                            # list of an article
                            text = (fp.read()).split()

                            #calling vocabulary method by passing text (list of words) and vocab as parameter.
                            self.vocabulary(text)

                # if not directory
                else:

                    with open(dirs[i], encoding='utf-8') as fp:

                        # list of an article
                        text = (fp.read()).split()

                        #calling vocabulary method by passing text (list of words) and vocab as parameter.
                        self.vocabulary(text)

            #list of unique words
            wordlist=list(self.vocab.keys())
            unique_count = len(wordlist)
            for x in range(unique_count):
                self.vocab[wordlist[x]][1] = x

            for i in range(fol):

                # if directory
                if os.path.isdir(dirs[i]):
                    isnumber = len(os.listdir(dirs[i]))
                    isnumbertotal = len(os.listdir(dirs[i]))
                    # no. of filename(documents)=no. of columns
                    files = os.listdir(dirs[i])
                    for filename in files:

                        row = np.zeros(unique_count, dtype=np.int8)  # initializing first row
                        with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
                            # print(filename, end="\r")
                            #list of an article
                            text = (fp.read()).split()
                            #initializing counter
                            cnt = Counter(text)
                            # print(cnt)
                            for key, value in cnt.items():
                                # print(self.vocab[key][1], key)
                                row[self.vocab[key][1]] = value
                            # print(row)
                            # for x in range(len(wordlist)):

                            #     # adding index of word in vocab dictionary
                            #     self.vocab[wordlist[x]][1]=x

                            #     if wordlist[x] in text:
                            #         row.append(cnt[wordlist[x]])
                            #     else:
                            #         row.append(0)
                            
                        hfcyvy ='\\'
                        print(f'{isnumber} left of {isnumbertotal} of {dirs[i].split(hfcyvy)[2]}                    ', end="\r")
                        isnumber-=1
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


if __name__ == "__main__":

    obj = TfidfVectorizer()
    # print(obj.__doc__)
    obj.documentTermMat(Path=".\\FilteredPreprocessed\\")
    obj.tf_idf()
    # obj.label()
    # print(obj.vocab)
    
    
    # print('.'*100)
    print(obj.vec)
    # print('.'*100)
    print(obj.result)
    # print('.'*100)
    # print(obj.label_dict)







