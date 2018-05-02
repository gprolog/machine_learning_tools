import os
import sys
import re
import json
import collections
import multiprocessing
from multiprocessing import Process, Manager,Pool
from keras.preprocessing import text
from dom_parser import *

sys.path.append(os.path.join('..','..'))
from utility.file_type_detector import *
from utility.encoding_checker import *
file_type_yara_file = os.path.join('..','..','utility','file_type.yar')

def is_legal_term(term):
    matched = re.findall(r'[^a-z]*', term)
    if matched:
        for item in matched:
            if len(item) > 0:
                return False
        return True
    else:
        return True

def remove_illegal_lines(input_file, output_file):
    with open(output_file, 'wb') as fh_output:
        with open(input_file, 'rb') as fh_input:
            for line in fh_input.readlines():
                key, value = line.split(':')
                if is_legal_term(key):
                    fh_output.write(line)

class WordGenerator:
    """
    """
    def __init__(self, config_map):
        self.max_tf_dict_ = {}
        self.total_tf_dict_ = {}
        self.max_term_len_ = 30
	self.config_map = config_map
        self.file_type_detector_ = FileTypeDetector(file_type_yara_file)
        self.encoding_modifier_ = EncodingModifier()
	self.dom_parser_ = DOMParser(config_map)

    def extract_html_script_content(self,content):
        self.dom_parser_.parse_content(content)
        js_list = self.dom_parser_.get_javascripts()
        vbs_list = self.dom_parser_.get_vbscripts()
        return '\n'.join(js_list) + '\n'.join(vbs_list)

    def extract_vbs_js_content(self, content):
        file_type, encoding_type = self.file_type_detector_.check_type(content)
        if FileType.FILETYPE_HTML == file_type:
            if EncodingType.ENCODE_UNKNOWN != encoding_type:
                content = self.encoding_modifier_.modify(content, encoding_type)
            return self.extract_html_script_content(content)
        elif FileType.FILETYPE_JS == file_type:
            return content
        elif FileType.FILETYPE_VBS == file_type:
            return content
        else:
            return content 
    
    def process(self, path):
        if os.path.isdir(path):
            print 'extract wording...'
            self.process_folder_with_multi_process(path)
        elif os.path.isfile(path):
            tf_dict = self.process_file(path)
            self.update_tf_dict(tf_dict)
        else:
            print('[WARN] Unknonw path type, {}'.format(path))

    def process_file(self, path):
        print('Process file: {}'.format(path))
        tf_dict = {}
        with open(path, 'rb') as fh:
	    content = fh.read()
	    if self.config_map['enable_extract_keyword_in_vbsjs']:
		print 'extract keyword in js and vbs...'
		content = self.extract_vbs_js_content(content)
	    else:
		print 'extract keyword in whole HTML...'
            words = text.text_to_word_sequence(content, filters='!"#$%&()*+,-.:;=?@[\\]^_`{|}~\t\r\n\'<>\/', \
                                              lower=True, split=" ")
            for item in words:
                try:
                    if len(item) > self.max_term_len_:
                        continue
                    if not is_legal_term(item):
                        continue
                    if item in tf_dict:
                        tf_dict[item] += 1
                    else:
                        tf_dict[item] = 1
                except Exception, e:
                    print(str(e))
                    print('item = {}'.format(item))
        return tf_dict

    def update_tf_dict(self, tf_dict):
        for (key, value) in tf_dict.items():
            # update max_tf_dict_
            if key in self.max_tf_dict_.keys():
                if value > self.max_tf_dict_[key]:
                    self.max_tf_dict_[key] = value
            else:
                self.max_tf_dict_[key] = value
            # update total_tf_dict_
            if key in self.total_tf_dict_.keys():
                self.total_tf_dict_[key] += value
            else:
                self.total_tf_dict_[key] = value

    def process_dir(self, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                tf_dict = self.process_file(os.path.join(root, name))
                self.update_tf_dict(tf_dict)

    def dump_key_frequence(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(os.path.join(output_dir, 'max_tf_list_script.txt'), 'wb') as fh:
            ordered_dict = collections.OrderedDict(sorted(self.max_tf_dict_.items(), key=lambda x: x[1], reverse=True))
            for item in ordered_dict:
                fh.write('{}:{}\n'.format(item, ordered_dict[item]))
        with open(os.path.join(output_dir, 'total_tf_list_script.txt'), 'wb') as fh:
            ordered_dict = collections.OrderedDict(sorted(self.total_tf_dict_.items(), key=lambda x: x[1], reverse=True))
            for item in ordered_dict:
                fh.write('{}:{}\n'.format(item, ordered_dict[item]))

    def process_folder_with_multi_process(self, src_dir):
        proc_num = multiprocessing.cpu_count()/2
        print 'process num=',proc_num
	file_list_map = {}
        ma = Manager()
        total_tf_map = {}
        max_tf_map = {}
        for i in range(0, proc_num):
            file_list_map[i] = []
            total_tf_map[i] = ma.dict()
            max_tf_map[i] = ma.dict()

        if os.path.isdir(src_dir):
            i = 0
            for root, dirs, files in os.walk(src_dir):
                for name in files:
		    #print 'file :', name
                    file_path = os.path.join(root, name)
                    file_list_map[i % proc_num].append(file_path)
                    i += 1
        else:
            print'[ERROR] multi-thread only process folder'
            exit(-1)

        proc_pool = []
        for i in range(0, proc_num):
            proc_pool.append(Process(target=self.process_file_path_list, args=(file_list_map[i], max_tf_map[i], total_tf_map[i])))

	for item in proc_pool:
            item.start() 
        
	for item in proc_pool:
	    item.join()

        for i in range(0, proc_num):
            for key in max_tf_map[i].keys():
                if self.max_tf_dict_.get(key) and len(key) > 3 and len(key) < 30:
                    if max_tf_map[i][key] > self.max_tf_dict_[key]:
                        self.max_tf_dict_[key] = max_tf_map[i][key]
                else:
                    self.max_tf_dict_[key] = max_tf_map[i][key]

            for key in total_tf_map[i].keys():
                if self.total_tf_dict_.get(key) and len(key) > 3 and len(key) < 30: 
                    self.total_tf_dict_[key] += total_tf_map[i][key]
                else:
                    self.total_tf_dict_[key] = total_tf_map[i][key]

        print "Exiting Main Process"

    def process_file_path_list(self, path_list, max_tf_map, total_tf_map):
	for path_ in path_list:
            print path_
	    tf_dict = self.process_file(path_)
            for (key, value) in tf_dict.items():
                # update max_tf_dict_
                if max_tf_map.get(key):
                    if value > max_tf_map[key]:
                        max_tf_map[key] = value
                else:
                    max_tf_map[key] = value
                # update total_tf_dict_
                if total_tf_map.get(key):
                    total_tf_map[key] += value
                else:
                    total_tf_map[key] = value

help_msg = """
Usage:
    (1) count maximum term number in sample_dir
    >> python tool.py -s sample_dir output_dir config_path
    (2) remove illegal lines from max_term_count_file
    >> python tool.py -r ori_term_count_file new_term_count_file
"""

if __name__ == '__main__':
    if sys.argv[1] == '-s':
	with open(sys.argv[4], 'rb') as fd:
	    config = json.load(fd)
        config_map = config['feature_extraction']
        wg = WordGenerator(config_map)
        wg.process(sys.argv[2])
        wg.dump_key_frequence(sys.argv[3])
    elif sys.argv[1] == '-r':
        remove_illegal_lines(sys.argv[2], sys.argv[3])
    else:
        print(help_msg)
