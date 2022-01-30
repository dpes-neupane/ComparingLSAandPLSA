from collections import Counter
import os

import numpy as np


class TfidfVectorizer():
    def __init__(self):
        self.input_list = []
        self.vocab = {}
        self.vec = None
        self.result = None



    def vocabulary(self, input_list, vocab)-> dict:
        self.input_list = input_list
        self.vocab = vocab
        x=[]
        for word in self.input_list:
            if word in self.vocab:
                self.vocab[word][0]+=1
            else:
                x=[1,0]
                self.vocab[word] = x
                
        return self.vocab
    
    def documentTermMat(self, Path=".\\preprocessed_test_data", input_text=''):
        # initializing dictionary for unique words in the documents
        self.vocab = {}
        mat = []
        # indexes=0
        if Path and not input_text:  # when path is given
            root = Path
            # list of dirs inside root
            dirs = [os.path.join(root, path) for path in os.listdir(root)]
            # num=0
            for i in range(len(dirs)):  # [education,health,sports,.....]
                # label=dirs[i][25:]
                # print(label)
                if os.path.isdir(dirs[i]):  # if directory

                    # education>>list of files(~2500)
                    # number_of_files = len(os.listdir(dirs[i]))
                    # num+=number_of_files
                    # print(label,i,": ",num)
                    for filename in os.listdir(dirs[i]):

                        with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
                            text = (fp.read()).split()  # list of an article
                            self.vocab = self.vocabulary(text,self.vocab)

                else:  # if not directory

                    with open(dirs[i], encoding='utf-8') as fp:
                        text = (fp.read()).split()

                        self.vocab = self.vocabulary(text,self.vocab)


            wordlist=list(self.vocab.keys())
            # print(type(wordlist))
            for i in range(len(dirs)):
                if os.path.isdir(dirs[i]):
                    # no. of filename(documents)=no. of columns
                    for filename in os.listdir(dirs[i]):
                        row = []  # initializing first row
                        with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
                            text = (fp.read()).split()
                            cnt = Counter(text)
                            # print(cnt['ट्रेजरी'])
                            for x in range(len(wordlist)):
                                self.vocab[wordlist[x]][1]=x
                                if wordlist[x] in text:
                                    row.append(cnt[wordlist[x]])
                                else:
                                    row.append(0)
                        mat.append(row)
        self.vec=np.array(mat)
    
    
    def tf_idf(self):
        tf= self.vec/self.vec.sum(axis=1)[:,np.newaxis]
        idf=np.log(self.vec.shape[0]/np.count_nonzero(self.vec,axis=0))
        # print(tf)
        # print('\n'*5)
        # print(idf)
        # print('\n'*5)
        self.result=tf*idf
        # print(self.result[:5,:20])

obj = TfidfVectorizer()
obj.documentTermMat()
obj.tf_idf()
print(obj.vocab)
print('.'*100)
print(obj.vec)
print('.'*100)
print(obj.result)

