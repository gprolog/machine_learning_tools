import os
import sys
import time
import json
from sklearn.datasets import load_svmlight_file
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np



def select(train_file,result_dir):
        # Build a classification task using 3 informative features
    X, y = load_svmlight_file(train_file)

        # Build a forest and compute the feature importances
    forest =  ExtraTreesClassifier(n_estimators=250, random_state=0)

    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]

        # Print the feature ranking
    #print("Feature ranking:")
 #  for f in range(X.shape[1]):
 #      print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    with open(os.path.join(result_dir, 'TFIDF_Contributeword.txt'),"w+") as fs:
        for f in range(X.shape[1]):
            select_word = "{0}.feature {1} ({2})".format(str(f + 1),str(indices[f]),str(importances[indices[f]]))
            fs.write(select_word)
            fs.write('\n')

def pri_help():
    print '''python tool.py TFIDF_FeatureList.txt resut_dir
'''

if __name__ == '__main__':
#    with open('/home/GT/automation/auto/md_auto_tools/src/machine_learning/training_process/config.json', 'rb') as fh:
 #       config = json.load(fh)
  #  helper = ClassifierHelper(config)
   # helper.score(sys.argv[1])
    pri_help()
    select(sys.argv[1],sys.argv[2]) 
