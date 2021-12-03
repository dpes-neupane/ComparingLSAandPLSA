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
    indexes=0
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
        for i in range(len(dirs)):
            if os.path.isdir(dirs[i]):
                # no. of filename(documents)=no. of columns
                for filename in os.listdir(dirs[i]):
                    row = []  # initializing first row
                    with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
                        text = (fp.read()).split()
                        cnt = Counter(text)
                        for word in wordlist:
                            if indexes<len(vocab):
                                vocab[word][1]+=indexes
                                indexes+=1
                            if word in text:
                                row.append(cnt[word])
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

    #     for word in vocab.keys():  # no of word = no. of rows
    #         row = []  # initializing first row
    #         for i in range(len(dirs)):
    #             if os.path.isdir(dirs[i]):
    #                 # no. of filename(documents)=no. of columns
    #                 for filename in os.listdir(dirs[i]):
    #                     with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
    #                         text = (fp.read()).split()
    #                         cnt = Counter(text)
    #                         # print(cnt)
    #                         # indexing the word as we go for may be future
    #                         vocab[word][1] = indexes
    #                         if word in text:  # check if the word is in document
    #                             # append the count of the word to row
    #                             row.append(cnt[word])
    #                         else:
    #                             row.append(0)  # append 0 if not
    #         mat.append(row)
    #         # making a multidimensional list for matrix generation
    #         # print(row)

    #         indexes += 1  # increase index for next word
    # vector=np.array(mat)
    # print(vector)
    # print(vector.shape)  # returns a numpy matrix for easy usage
    # print(vocab["बर्ष"])
    # print(vector[157:158,:])
    #     for word in vocab.keys():  # word in corpus
    #         print(word, end='\t')

    #         for i in range(len(dirs)):

    #             if os.path.isdir(dirs[i]):

    #                 for filename in os.listdir(dirs[i]):
    #                     with open(os.path.join(dirs[i], filename), encoding='utf-8') as fp:
    #                         text = (fp.read()).split()
    #                         indexes = 0
    #                         # to count number of words in document
    #                         cnt = Counter(text)
    #                         vocab[word][1] = indexes
    #                         indexes += 1

    #             else:

    #                 for i in range(len(dirs)):

    #                     with open(dirs[i], encoding='utf-8') as fp:
    #                         text = (fp.read()).split()
    #                         # to count number of words in document
    #                         cnt = Counter(text)
    #                         print(cnt[word], end='\t')
    #         print('\n')

# root=r'E:\Project\NewsTextClassifierSeventhProject\16NepaliNews\raw'
# dirs=[os.path.join(root, path) for path in os.listdir(root)]
# print(dirs)
# with open("text.csv", "w") as fp:
#     fp.write("s.n.")
#     for i in range(len(dirs)):
#         for filename in os.listdir(dirs[i]):
#             fp.write(',')
#             fp.write(filename)
#     for word in vocab.keys():  # word in corpus
#         print(word, end = '\t')

#         for i in range(len(dirs)):

#             if os.path.isdir(dirs[i]):

#                 for filename in os.listdir(dirs[i]):

#                     with open(os.path.join(dirs[i], filename), encoding = 'utf-8') as fp:
#                         text=(fp.read()).split()
#                         # to count number of words in document
#                         cnt=Counter(text)
#                         print(cnt[word], end = '\t')
#             else:

#                 for i in range(len(dirs)):

#                     with open(dirs[i], encoding = 'utf-8') as fp:
#                         text=(fp.read()).split()
#                         # to count number of words in document
#                         cnt=Counter(text)
#                         print(cnt[word], end = '\t')
#         print('\n')

#     fp.write("\n")



documentTermMat()