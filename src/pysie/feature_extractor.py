import os
import sys
import json
from dom_parser import *
from js_feature_extractor import *
from vbs_feature_extractor import *
from keyword_feature_analyzer import *
from tfidf import *
sys.path.append(os.path.join('..','..'))
from utility.file_type_detector import *
from utility.encoding_checker import *
file_type_yara_file = os.path.join('..','..','utility','file_type.yar')

class FeatureExtractor:
    def __init__(self, feature_config_path):
        with open(feature_config_path, 'r+') as fd:
            self.feature_cfg = json.load(fd)
        self.feature_cfg_map = self.feature_cfg['feature_extraction']
        self.file_type_detector_ = FileTypeDetector(file_type_yara_file)
        self.encoding_modifier_ = EncodingModifier()
        self.dom_parser_ = DOMParser(self.feature_cfg_map)
    
    def get_jsvbs_content(self, content):
        file_type, encoding_type = self.file_type_detector_.check_type(content)
        try:
            if FileType.FILETYPE_HTML == file_type:
                dom_parser_ = DOMParser(self.feature_cfg_map)
                dom_parser_.parse_content(content)
                js_list = dom_parser_.get_javascripts()
                vbs_list = dom_parser_.get_vbscripts()
                content = '\n'.join(js_list) + '\n'.join(vbs_list)            
                return content
            elif FileType.FILETYPE_JS == file_type:
                return content
            elif FileType.FILETYPE_VBS == file_type:
                return content
            else:
                return None
        except UnicodeEncodeError:
            print( 'got unicode encode error')
        except UnicodeDecodeError:
            print( 'got unicode decode error')
        except BaseException:
            print( 'got exception')
