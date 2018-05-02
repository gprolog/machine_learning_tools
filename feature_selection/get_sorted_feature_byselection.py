import sys
import os
import json
from collections import OrderedDict

# use Tree-based feature selection http://scikit-learn.org/stable/modules/feature_selection.html#feature-selection
newindex_oldindex = {}
wordindexdict = {}
indexequence = []
words = []
words_tfidf = {}
wordcount_dict = {}

def get_feature_tfidf_dict(tfidf_list, wordindex, wordcount, contrilist, sample_path):
    global words_tfidf,wordindexdict,wordcount_dict,indexequence
    max_tfidf_val = 0.0
    count = 0.0
    for root, dirs, files in os.walk(sample_path):
        for sigle_file in files:
            count = count + 1
   # print count
    up_num = (4.0/5)*count
    down_num = (1.0/10000)*count
   # print up_num
   # print down_num
    with open(tfidf_list, 'r+') as fd:
        while True:
            try:
                line = fd.readline()
            except UnicodeDecodeError:
                continue
            if not line:
                break
            line = line.rstrip('\n')
            key = line[:line.find(':')]
            if not len(key) > 2:
                continue
            try:
                value = float(line[line.find(':')+1:])
		if value > max_tfidf_val:  # tfidf_list is a sorted list, and the first line is the max tfidf value
                    max_tfidf_val = value
                   # print max_tfidf_val
                words_tfidf[key] = value/max_tfidf_val
            except ValueError:
                pass

    with open(wordindex, 'r+') as fd:
        while True:
            try:
                line = fd.readline()
            except UnicodeDecodeError:
                continue
            if not line:
                break
            line = line.rstrip('\n')
            key = line[:line.find(':')]
            if not len(key) > 2:
                continue
            try:
                value = int(line[line.find(':') + 1:])
                wordindexdict[value] = key
            except ValueError:
                pass

    with open(wordcount, 'r+') as fd:
        while True:
            try:
                line = fd.readline()
            except UnicodeDecodeError:
                continue
            if not line:
                break
            line = line.rstrip('\n')
            key = line[:line.find(':')]
            if not len(key) > 2:
                continue
            try:
                value = int(line[line.find(':') + 1:])
                wordcount_dict[key] = value
            except ValueError:
                pass

    with open(contrilist, 'r+') as fd:
        lines = fd.readlines()
        for line in lines:
            line = line.rstrip('\n')
            if not len(line) > 2:
                continue
            indexequence.append(int(line[line.find('feature') + len('feature'):line.find('(') - 1]))

    num = 0
    root, f = os.path.split(tfidf_list)
    with open(os.path.join(root, 'TFIDF_NewContrilist_new.txt'), 'w+') as fd:
        with open(os.path.join(root, 'html.yar'), 'w+') as fh:
            for index in indexequence:
                try:
                    word = wordindexdict[index]
                    if not 3 < len(word) < 30:
                        continue
                    if not up_num > wordcount_dict[word] > down_num:
                        continue
                    line = "\"" + wordindexdict[index] + "\":" + str(words_tfidf[word]) + ',\n'
                    fd.write(line)

                    rule = '''
rule keyword_{0}{{
    meta:
        index="{1}"
        TFIDF="{2}"
    strings:
        $s="{0}" fullword nocase
    condition:
        $s
    }}

 '''.format(word, str(num), words_tfidf[word])
                    fh.write(rule)
                    num += 1
                    if num > 10000:
                        break
                except KeyError:
                    continue
                except UnicodeEncodeError:
                    continue
                except UnicodeDecodeError:
                    continue

def print_help():
    print '''
	python tool.py tfidf_sorted_list wordindex wordcount tfidf_contributeword sample_path'''
    
if __name__ == '__main__':
    try:
        get_feature_tfidf_dict(sys.argv[1], sys.argv[2], sys .argv[3], sys.argv[4], sys.argv[5])
    except:
        print_help()
