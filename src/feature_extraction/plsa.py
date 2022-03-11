import numpy as np



class PLSA():
    '''here,
    n = the number of documents in teh corpus
    z = number of clusters (topics)
    w = number of distinct words in teh corpus
    TDMat = Term-document matrix (an numpy array)'''

    def __init__(self, n:int , z:int, w: int, TDmat) -> None:
        self.n_doc = n
        self.z_topics = z
        self.w_words = w
        self.TDmat = TDmat


    def __normalize(self, matrix):
        '''this function returns a normalized matrix whose row sum to 1'''
        #this calculates teh sum of each row and puts it in a matrix
        row_matrix_sum = matrix.sum(axis=1)
        assert (np.count_nonzero(row_matrix_sum) == row_matrix_sum.shape[0]), "there are rows which sum to 0"
        return matrix/row_matrix_sum[:, np.newaxis]


    def initialize(self) -> None:
        '''this function should initialize the P(d|z), P(z) and P(w|z) matrices with random values.
        P(d|z) = self.prob_document_G_topic
        P(w|z) = self.prob_words_G_topic'''
        self.prob_document_G_topic = self.__normalize(np.random.random(size= (self.n_doc, self.z_topics)).astype(np.float32))
        self.prob_words_G_topic = self.__normalize(np.random.random(size=(self.z_topics, self.w_words)).astype(np.float32))
        self.topic_prob_G_doc_w = np.zeros(shape=(self.n_doc, self.z_topics, self.w_words), dtype=np.float16)


    def expectation_step(self) -> None:
        '''the expectation step calculates teh posterior probability P(z | d, w)'''
        self.topic_prob_G_doc_w = np.nan_to_num(self.topic_prob_G_doc_w)

        for doc in range(self.n_doc):
            for word in range(self.w_words):
                self.topic_prob_G_doc_w[doc, :, word] = self.prob_document_G_topic[doc, :] * self.prob_words_G_topic[:, word]
                self.topic_prob_G_doc_w[doc, :, word] /= self.topic_prob_G_doc_w[doc, :, word].sum()

        self.topic_prob_G_doc_w = np.nan_to_num(self.topic_prob_G_doc_w)


    def maximization_step(self) -> None:
        '''The M-step updates  P(w|z) and P(z|d)'''
        print("M-step....")
        print("updating P(z|d)")

        for doc in range(self.n_doc):
            for topic in range(self.z_topics):
                self.prob_document_G_topic[doc, topic] = self.TDmat[doc, :]  @ self.topic_prob_G_doc_w[doc, topic, :]
            self.prob_document_G_topic[doc, :] /= self.prob_document_G_topic[doc, :].sum()
        self.prob_document_G_topic = np.nan_to_num(self.prob_document_G_topic)

        print("\nupdating P(w|z)")

        for topic in range(self.z_topics):
            for word in range(self.w_words):
                self.prob_words_G_topic[topic, word] = self.TDmat[:, word] @ self.topic_prob_G_doc_w[:, topic, :]
            self.prob_words_G_topic[:, word] /= self.prob_words_G_topic[:, word].sum()
        self.prob_words_G_topic = np.nan_to_num(self.prob_words_G_topic)


    def log_likelihood(self) -> float:
        '''Calculate the current log-likelihood using the updated probability matrices'''

        return np.sum(np.log(self.prob_document_G_topic @ self.prob_words_G_topic) * self.TDmat)

    def plsa(self, max_iter:int, epsilon:float):
        '''max_iter = the number of iterations the log_likelihood is calculated
           epsilon = the absolute difference between the current likelihood and last likelihood that is tolerated'''
        self.initialize()

        current_likelihood = 0.0


        for iteration in range(max_iter):
            self.expectation_step()
            self.maximization_step()

            tmp_likelihood = self.log_likelihood()
            if iteration > 100 and abs(current_likelihood - tmp_likelihood) < epsilon / 10:
                print("Stopping", tmp_likelihood)
                return tmp_likelihood
            current_likelihood = tmp_likelihood
        return self.topic_prob_G_doc_w