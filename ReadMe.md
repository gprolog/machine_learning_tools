Model Training and Scoring
===============

Platform and Pre-installation
------
1. Ubuntu 16.04 and python 2.7.*
2. Python Machine Learning Toolkit(sckit, xgboost, keras)


Usage
------
```python
python auto_engine.py
```

Before executing automation script, please set training_test_set and mid_folder in auto.json

Such as following example:

```json
 {
  "auto_by_engine":{
         "_comment":"word freq function TFIDF|Pure|MAXTF",
         "word_freq_function":"Pure",
         "middle_dir":"/home/leon/1105",
         "train_test_set_path":"/home/sample/train_test_for_test",
         "enable_extract_feature":1,
          "engine_extract_feature_cfg":{
                "use_top_keyword":0,
                "start_extract_index":0,
                "extract_interval":100
          }
  }
```


Need more info please following:
https://wiki.jarvis.trendmicro.com/display/SA/How+to+use+machine+learning+tools
