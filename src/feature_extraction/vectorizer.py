import os
from collections import Counter
from matplotlib.pyplot import axis
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
                        vocab = vocabulary(text,vocab)

            else:  # if not directory

                with open(dirs[i], encoding='utf-8') as fp:
                    text = (fp.read()).split()

                    vocab = vocabulary(text,vocab)


        wordlist=list(vocab.keys())
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
                            vocab[wordlist[x]][1]=x
                            if wordlist[x] in text:
                                row.append(cnt[wordlist[x]])
                            else:
                                row.append(0)
                    mat.append(row)
    vec=np.array(mat)
    # print(vocab)
    print(vec)

    print('\n'*5)


    # print(vec.shape)  # returns a numpy matrix for easy usage
    # print(vec[0,:50])
    # print(len(vocab))
    # print(vocab['नेपाल'])
    # print(vec.sum(axis=0)[:10])
    # print(vocab["बैंक"])
    # print(vocab["जारी"])

    # print(vocab['राष्ट्र'])
    # # print(vocab['अर्ब'])

    # # tf= vec/vec.sum(axis=0)
    # # print(vec)
    # # print(tf)
    # # y=tf.shape[0]
    # # print(y)

    # print(wordlist[:10])
    # print(cnt['ट्रेजरी'])

documentTermMat()
print(np.log2(4))

def tf_idf(vec):
    tf=vec/vec.sum(axis=1)[:,np.newaxis]
    idf=np.log(vec.shape[0]/np.count_nonzero(vec,axis=0))
    print(tf)
    print('\n'*5)
    print(idf)
    print('\n'*5)
    tf_idf=tf*idf
    print(tf_idf[:5,:20])