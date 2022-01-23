import os
from collections import Counter
import numpy as np
# coding = utf-8

def vocabulary(input_list, vocab):
    x=[]
    for word in input_list:
        if word in vocab:
            vocab[word][0]+=1
        else:
            x=[1,0]
            vocab[word] = x
    return vocab


def documentTermMat(Path=".\\preprocessed_test_data", input_text=''):
    # initializing dictionary for unique words in the documents
    vocab = {}
    mat = []
    # indexes=0
    if Path and not input_text:  # when path is given
        root = Path
        # list of dirs inside root
        dirs = [os.path.join(root, path) for path in os.listdir(root)]
        # print(dirs)
        for i in range(len(dirs)):  # [education,health,sports,.....]

            if os.path.isdir(dirs[i]):  # if directory

                # education>>list of files(~2500)
                for filename in os.listdir(dirs[i]):

                    with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
                        text = (fp.read()).split()  # list of an article
                        vocab = vocabulary(text,vocab)

            else:  # if not directory

                with open(dirs[i], encoding='utf-8') as fp:
                    text = (fp.read()).split()

                    vocab = vocabulary(text,vocab)
        wordlist=vocab.keys()
        print(type(wordlist))
        for i in range(len(dirs)):
            if os.path.isdir(dirs[i]):
                # no. of filename(documents)=no. of columns
                for filename in os.listdir(dirs[i]):
                    row = []  # initializing first row
                    with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
                        text = (fp.read()).split()
                        cnt = Counter(text)
                        for i in range(len(wordlist)):
                            if i<len(vocab):
                                vocab[wordlist[i]][1]=i

                            if wordlist[i] in text:
                                row.append(cnt[wordlist[i]])
                            else:
                                row.append(0)
                    mat.append(row)
    vector=np.array(mat)
    # print(vocab)
    print(vector)
    print(vector.shape)  # returns a numpy matrix for easy usage
    print(len(vocab))
    print(vocab['नेपाल'])
    print(vocab["बर्ष"])
    print(vocab['राष्ट्र'])
    print(vocab['अर्ब'])
    print(vector[:1,:30])
    tran=vector.transpose()
    print(tran)
    print(tran.shape)




documentTermMat()