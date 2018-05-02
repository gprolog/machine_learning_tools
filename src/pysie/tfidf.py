#-*-coding:utf8-*-
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing import text
from collections import OrderedDict
import codecs
import os
import chardet
import random
from array import *
import math

max_word_length = 20
min_word_length = 3


class TFIDFExtractor:
    def __init__(self, sample_folder, topn, resultdir):
        self._sample_folder = sample_folder
        self._topn = topn # select the topn keywords by tfidf value
        self._to_vectorize_word = []   # the word is filtered by simple rule (max_word_length > length > min_word_length)
        self._words = []
        self._wordweight = [[]]
        self._topn_word = {}
        self.process_num = 0
        self.word_count_inset_dict = {}
        self.tf_word_dict = {}
        self.idf_word_dict = {}
        self.tfidf_word_dict = {}
        self._resultdir = resultdir
        self._unsorted_word = OrderedDict()
        self.filecount = 0
        self.maxtfidf = 0
        self.matrix_ ={}
        self.matrix_[1] = []
        self.matrix_[0] = []        

    def extract_word_vector(self):
        for root, dirs, samples in os.walk(self._sample_folder):
            for sample in samples:
                with open(os.path.join(root, sample), 'r+') as fd:
                    words = text.text_to_word_sequence(fd.read().decode('gb2312').encode('utf8'),
                                               filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                               lower=True,
                                               split=" ")
                    line = ''
                    for word in words:
                        if min_word_length < len(word) < max_word_length:
                            line += word + ' '
                    line.rstrip(' ')
                    self._to_vectorize_word.append(line)

    def extract_content_vector(self, content, samplepath, label):
        words = text.text_to_word_sequence(content,
                                       filters='1234567890!\'"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r',
                                       lower=True,
                                       split=" ")
        len_word = len(words)
        #words = map(remove_enter_in_window,words) 
        words = filter(lambda x: min_word_length < len(x) < max_word_length, list(words))
        temp_dict = {}
        wordset = set(words)
        for word in wordset:
            if self.word_count_inset_dict.get(word) is not None:
                self.word_count_inset_dict[word] += 1
            else:
                self.word_count_inset_dict[word] = 1
            temp_dict[word] = words.count(word)

        for word in wordset:
            if self.tf_word_dict.get(word) is None:
                self.tf_word_dict[word] = temp_dict[word]/(len_word*1.0 + 1.0)
            else:
                if self.tf_word_dict[word] < temp_dict[word]/(len_word*1.0 + 1.0):
                    self.tf_word_dict[word] = temp_dict[word]/(len_word*1.0 + 1.0)
            
        if label == 1:
            self.matrix_[1].append(wordset)
        else:
            self.matrix_[0].append(wordset)
            
        self.filecount += 1
        self.process_num += 1
        if self.process_num%1000 == 0:
            print('have processed:', self.process_num)
        #line = ' '.join(words)
        #self._to_vectorize_word.append(line)   # the word is filtered by simple rule (max_word_length > length > min_word_length)
        


    def compute_tfidf(self):
        print('compute tfidf')
        for word in self.tf_word_dict.keys():
            self.tfidf_word_dict[word] = self.tf_word_dict[word] * math.log((self.filecount/(self.word_count_inset_dict[word]*1.0 + 1.0)))        #add 1.0 incase doc contain word is 0

    def dump_topn_word_tofile(self):
        ordered_dict = OrderedDict(sorted(self.tfidf_word_dict.items(), key=lambda x: x[1], reverse=True))
        if not os.path.exists(self._resultdir):
            os.makedirs(self._resultdir)
        with open(os.path.join(self._resultdir, 'TFIDF_Sorted.txt'), 'w+') as fd:
            for key, value in ordered_dict.items():
                try:
                    fd.write((key +':' + str(value)))
                    fd.write('\n')
                except UnicodeEncodeError:
                   pass 
        '''with open(os.path.join(self._resultdir, 'TFIDF_UnSorted.txt'), 'w+') as fd:
            for key, value in self._unsorted_word.items():
                try:
                    fd.write((key +':' + str(value)))
                    fd.write('\n')
                except UnicodeEncodeError:
                    pass
        '''
        with open(os.path.join(self._resultdir, 'TFIDF_WordCount.txt'), 'w+') as fd:
            for key, value in self.word_count_inset_dict.items():
                try:
                    fd.write((key +':' + str(value)))
                    fd.write('\n')
                except UnicodeEncodeError:
                    pass
        self.dump_matrix()

    def dump_matrix(self):
        self.word_index = {}
        index = 0
        for word in self.tfidf_word_dict.keys():
            self.word_index[word] = index
            index += 1
        with open(os.path.join(self._resultdir, "TFIDF_WordIndex.txt"), 'w+') as fd:
            for word in self.word_index:
                try:
                    line = word + ':' + str(self.word_index[word])  + '\n'
                    fd.write(line)
                except UnicodeEncodeError:
                    pass
        with open(os.path.join(self._resultdir, 'TFIDF_FeatureList.txt'), 'w+') as fd:
            for label in self.matrix_.keys():
                    for l in self.matrix_[label]:
                        temp_dict = {}
                        for word in l:
                            temp_dict[self.word_index[word]] = self.tfidf_word_dict[word]
                        sl = sorted(temp_dict.keys())
                        line = str(label) + ' '
                        for index in sl:
                            try:
                                line += str(index) + ':' + str(temp_dict[index]) + ' '
                            except UnicodeEncodeError:
                                pass
                        fd.write(line)
                        fd.write('\n')

        
    def auto(self):
        self.extract_word_vector()
        self.compute_tfidf()
        self.extracto_topn_keyword()
        self.dump_topn_word_tofile()

if __name__ == '__main__':
    tfidf = TFIDFExtractor('/home/GT/sample/for_test/mal_set/', 1000)
    tfidf.auto()        