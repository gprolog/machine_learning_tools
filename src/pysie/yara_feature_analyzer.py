#
import yara
import json

class YaraFeatureAnalyzer:
    """extract feature by YARA rules"""
    def __init__(self, feature_rules):
        self.yara_rules_ = yara.compile(source=feature_rules)
        self.matched_feature_index_map_ = {}

    def analyze_content(self, content, base_index):
        matched_rules = self.yara_rules_.match(data=content)
        for matched in matched_rules:
            index_value = matched.meta['index']
            if matched.rule.startswith('malicious_'):
                index_value = index_value + base_index
            self.matched_feature_index_map_[index_value] = 1

    def get_features(self):
        return self.matched_feature_index_map_

def print_help():
    pass

if __name__ == '__main__':
    cfg_file = r'pysie.cfg'
    with open(cfg_file, 'rb') as fh:
        config_map = json.load(fh)
    content = """
    payload and shellcode
    """
    # test js yara rules
    js_feature_yara_rule = config_map['feature_extraction']['js_feature_yara_rule']
    with open(js_feature_yara_rule, 'rb') as fh:
        feature_rules = fh.read()
    yara_fea_analyzer = YaraFeatureAnalyzer(feature_rules)
    yara_fea_analyzer.analyze_content(content, config_map['feature_extraction']['js_base_index'])
    print(yara_fea_analyzer.get_features())

    # test vbs yara rules
    vbs_feature_yara_rule = config_map['feature_extraction']['vbs_feature_yara_rule']
    with open(vbs_feature_yara_rule, 'rb') as fh:
        vbs_feature_rules = fh.read()
    vbs_yara_fea_analyzer = YaraFeatureAnalyzer(vbs_feature_rules)
    vbs_yara_fea_analyzer.analyze_content(content, config_map['feature_extraction']['vbs_base_index'])
    print(vbs_yara_fea_analyzer.get_features())