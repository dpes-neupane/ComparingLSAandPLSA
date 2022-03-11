# import numpy as np



# class PLSA():
#     '''here,
#     n = the number of documents in teh corpus
#     z = number of clusters (topics)
#     w = number of distinct words in teh corpus
#     TDMat = Term-document matrix (an numpy array)'''

#     def __init__(self, n:int , z:int, w: int, TDmat) -> None:
#         self.n_doc = n
#         self.z_topics = z
#         self.w_words = w
#         self.TDmat = TDmat


#     def __normalize(self, matrix):
#         '''this function returns a normalized matrix whose row sum to 1'''
#         #this calculates teh sum of each row and puts it in a matrix
#         row_matrix_sum = matrix.sum(axis=1)
#         assert (np.count_nonzero(row_matrix_sum) == row_matrix_sum.shape[0]), "there are rows which sum to 0"
#         return matrix/row_matrix_sum[:, np.newaxis]


#     def initialize(self) -> None:
#         '''this function should initialize the P(d|z), P(z) and P(w|z) matrices with random values.
#         P(d|z) = self.prob_document_G_topic
#         P(w|z) = self.prob_words_G_topic'''
#         self.prob_document_G_topic = self.__normalize(np.random.random(size= (self.n_doc, self.z_topics)).astype(np.float32))
#         self.prob_words_G_topic = self.__normalize(np.random.random(size=(self.z_topics, self.w_words)).astype(np.float32))
#         self.topic_prob_G_doc_w = np.zeros(shape=(self.n_doc, self.z_topics, self.w_words), dtype=np.float16)


#     def expectation_step(self) -> None:
#         '''the expectation step calculates teh posterior probability P(z | d, w)'''
#         self.topic_prob_G_doc_w = np.nan_to_num(self.topic_prob_G_doc_w)

#         for doc in range(self.n_doc):
#             for word in range(self.w_words):
#                 self.topic_prob_G_doc_w[doc, :, word] = self.prob_document_G_topic[doc, :] * self.prob_words_G_topic[:, word]
#                 self.topic_prob_G_doc_w[doc, :, word] /= self.topic_prob_G_doc_w[doc, :, word].sum()

#         self.topic_prob_G_doc_w = np.nan_to_num(self.topic_prob_G_doc_w)


#     def maximization_step(self) -> None:
#         '''The M-step updates  P(w|z) and P(z|d)'''
#         print("M-step....")
#         print("updating P(z|d)")

#         for doc in range(self.n_doc):
#             for topic in range(self.z_topics):
#                 self.prob_document_G_topic[doc, topic] = self.TDmat[doc, :]  @ self.topic_prob_G_doc_w[doc, topic, :]
#             self.prob_document_G_topic[doc, :] /= self.prob_document_G_topic[doc, :].sum()
#         self.prob_document_G_topic = np.nan_to_num(self.prob_document_G_topic)

#         print("\nupdating P(w|z)")

#         for topic in range(self.z_topics):
#             for word in range(self.w_words):
#                 self.prob_words_G_topic[topic, word] = self.TDmat[:, word] @ self.topic_prob_G_doc_w[:, topic, :]
#             self.prob_words_G_topic[:, word] /= self.prob_words_G_topic[:, word].sum()
#         self.prob_words_G_topic = np.nan_to_num(self.prob_words_G_topic)


#     def log_likelihood(self) -> float:
#         '''Calculate the current log-likelihood using the updated probability matrices'''

#         return np.sum(np.log(self.prob_document_G_topic @ self.prob_words_G_topic) * self.TDmat)

#     def plsa(self, max_iter:int, epsilon:float):
#         '''max_iter = the number of iterations the log_likelihood is calculated
#            epsilon = the absolute difference between the current likelihood and last likelihood that is tolerated'''
#         self.initialize()

#         current_likelihood = 0.0


#         for iteration in range(max_iter):
#             self.expectation_step()
#             self.maximization_step()

#             tmp_likelihood = self.log_likelihood()
#             if iteration > 100 and abs(current_likelihood - tmp_likelihood) < epsilon / 10:
#                 print("Stopping", tmp_likelihood)
#                 return tmp_likelihood
#             current_likelihood = tmp_likelihood
#         return self.topic_prob_G_doc_w






import numpy as np
import math


def normalize(input_matrix):
    """
    Normalizes the rows of a 2d input_matrix so they sum to 1
    """

    row_sums = input_matrix.sum(axis=1)

    for row in row_sums:
        if row == 0:
            print(row)
    assert (np.count_nonzero(row_sums) == np.shape(row_sums)[0])
    # no row should sum to zero
    new_matrix = input_matrix / row_sums[:, np.newaxis]
    return new_matrix


class Corpus(object):
    """
    A collection of documents.
    """

    def __init__(self,  term_doc_matrix, documents_path=""):
        """
        Initialize empty document list.
        """
        self.documents = []
        self.vocabulary = []
        self.likelihoods = []
        self.documents_path = documents_path
        self.term_doc_matrix = term_doc_matrix
        self.document_topic_prob = None  # P(z | d)
        self.topic_word_prob = None  # P(w | z)
        self.topic_prob = None  # P(z | d, w)

        self.number_of_documents = term_doc_matrix.shape[0]
        self.vocabulary_size = term_doc_matrix.shape[1]
        self.vocabulary_dist = {}

    def build_corpus(self):
        """
        Read document, fill in self.documents, a list of list of word
        **************************************************
        *** Here assumes the doc is in .txt format and each line represent one document
        *** If it's not the case, edit this part.
        **************************************************
        self.documents = [["the", "day", "is", "nice", "the", ...], [], []...]
        Update self.number_of_documents
        """
        # #############################
        # your code here
        # #############################
        print(self.documents_path)
        with open(self.documents_path, 'r') as file:
            for line in file.readlines():
                doc = list()
                doc.extend(line.split())
                self.documents.append(doc)
                # self.documents.append(doc)
                self.number_of_documents += 1

        # print(self.documents)
        print(len(self.documents))
        print(self.number_of_documents)

    def build_vocabulary(self):
        """
        Construct a list of unique words in the whole corpus. Put it in self.vocabulary
        for example: ["rain", "the", ...]
        Update self.vocabulary_size
        """
        # #############################
        # your code here
        # #############################
        res = set()
        for doc in self.documents:
            res.update(doc)
        self.vocabulary = res
        self.vocabulary_size = len(res)
        self.vocabulary_dist = {k: i for i, k in enumerate(self.vocabulary)}

    def build_term_doc_matrix(self):
        """
        Construct the term-document matrix where each row represents a document,
        and each column represents a vocabulary term.
        self.term_doc_matrix[i][j] is the count of term j in document i
        """
        # ############################
        # your code here
        # ############################
        self.term_doc_matrix = np.zeros(shape=(self.number_of_documents, self.vocabulary_size))

        for i, doc in enumerate(self.documents):
            for term in doc:
                self.term_doc_matrix[i][self.vocabulary_dist[term]] += 1
        # print(self.term_doc_matrix)

    def initialize_randomly(self, number_of_topics):
        """
        Randomly initialize the matrices: document_topic_prob and topic_word_prob
        which hold the probability distributions for P(z | d) and P(w | z): self.document_topic_prob, and self.topic_word_prob
        Don't forget to normalize!
        HINT: you will find numpy’s random matrix useful [https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.random.html]
        """
        # ############################
        # your code here
        # ############################
        print("doc  topic.....")

        self.document_topic_prob = normalize(np.random.random(size=(self.number_of_documents, number_of_topics)))
        print("topic word.....")
        self.topic_word_prob = normalize(np.random.random(size=(number_of_topics, self.vocabulary_size)))

    def initialize_uniformly(self, number_of_topics):
        """
        Initializes the matrices: self.document_topic_prob and self.topic_word_prob with a uniform
        probability distribution. This is used for testing purposes.
        DO NOT CHANGE THIS FUNCTION
        """
        self.document_topic_prob = np.ones((self.number_of_documents, number_of_topics))
        self.document_topic_prob = normalize(self.document_topic_prob)

        self.topic_word_prob = np.ones((number_of_topics, len(self.vocabulary)))
        self.topic_word_prob = normalize(self.topic_word_prob)

    def initialize(self, number_of_topics, random=True):
        """ Call the functions to initialize the matrices document_topic_prob and topic_word_prob
        """
        print("Initializing...")

        if random:
            self.initialize_randomly(number_of_topics)
        else:
            self.initialize_uniformly(number_of_topics)

    def expectation_step(self):
        """ The E-step updates P(z | w, d) self.topic_prob
        """
        print("E step:")

        #############################
        # your code here            #
        #############################
        self.topic_word_prob = np.nan_to_num(self.topic_word_prob)
        for doc in range(self.topic_prob.shape[0]):
            for voc in range(self.topic_prob.shape[2]):
                self.topic_prob[doc, :, voc] = self.document_topic_prob[doc, :] * self.topic_word_prob[:, voc]
                self.topic_prob[doc, :, voc] /= self.topic_prob[doc, :, voc].sum()
        self.topic_word_prob = np.nan_to_num(self.topic_word_prob)

    def maximization_step(self, number_of_topics):
        """ The M-step updates P(w | z)
        """
        print("M step:")

        # update P(w | z)

        # ############################
        # your code here
        # ############################
        for topic in range(self.topic_prob.shape[1]):
            for voc in range(self.topic_prob.shape[2]):
                self.topic_word_prob[topic, voc] = self.term_doc_matrix[:, voc].dot(self.topic_prob[:, topic, voc])
            self.topic_word_prob[topic, :] /= self.topic_word_prob[topic, :].sum()
        self.topic_word_prob = np.nan_to_num(self.topic_word_prob)

        # print('hello world')
        # print (self.topic_word_prob)
        # print('hello world')
        # update P(z | d)

        # ############################
        # your code here
        # ############################
        for doc in range(self.topic_prob.shape[0]):
            for topic in range(self.topic_prob.shape[1]):
                self.document_topic_prob[doc, topic] = self.term_doc_matrix[doc, :].dot(self.topic_prob[doc, topic, :])
            self.document_topic_prob[doc, :] /= self.document_topic_prob[doc, :].sum()
        self.document_topic_prob = np.nan_to_num(self.document_topic_prob)

    def calculate_likelihood(self, number_of_topics):
        """ Calculate the current log-likelihood of the model using
        the model's updated probability matrices
        Append the calculated log-likelihood to self.likelihoods
        """
        # ############################
        # your code here             #
        # ############################
        self.likelihoods.append(np.sum(np.log(self.document_topic_prob @ self.topic_word_prob) * self.term_doc_matrix))
        return self.likelihoods[-1]

    def plsa(self, number_of_topics, max_iter, epsilon):

        """
        Model topics.
        """
        print("EM iteration begins...")

        # build term-doc matrix
        # self.build_term_doc_matrix()

        # Create the counter arrays.

        # P(z | d, w)
        self.topic_prob = np.zeros([self.number_of_documents, number_of_topics, self.vocabulary_size], dtype=np.float)

        # P(z | d) P(w | z)
        self.initialize(number_of_topics, random=True)
        # print (self.document_topic_prob[:10,:10], self.topic_word_prob[:10, :10])

        # Run the EM algorithm
        current_likelihood = 0.0

        last_topic_prob = self.topic_prob.copy()

        for iteration in range(max_iter):
            print("Iteration #" + str(iteration + 1) + "...")

            # ############################
            # your code here
            # ############################
            self.expectation_step()
            diff = abs(self.topic_prob - last_topic_prob)
            L1 = diff.sum()
            print ("L1: ", L1)
            # print (last_topic_prob)
            # assert L1 > 0
            last_topic_prob = self.topic_prob.copy()

            self.maximization_step(number_of_topics)
            self.calculate_likelihood(number_of_topics)
            tmp_likelihood = self.calculate_likelihood(number_of_topics)
            if iteration > 100 and abs(current_likelihood - tmp_likelihood) < epsilon/10:
                print('Stopping', tmp_likelihood)
                return tmp_likelihood
            current_likelihood = tmp_likelihood
            print(max(self.likelihoods))
