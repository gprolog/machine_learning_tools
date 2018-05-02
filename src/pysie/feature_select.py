import os
import sys
import time
import json
from sklearn.datasets import load_svmlight_file
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np



def select(train_file):
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

    for f in range(X.shape[1]):
        #self.__select_feature_list.append(indices[f])
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

if __name__ == '__main__':
#    with open('/home/GT/automation/auto/md_auto_tools/src/machine_learning/training_process/config.json', 'rb') as fh:
 #       config = json.load(fh)
  #  helper = ClassifierHelper(config)
   # helper.score(sys.argv[1])
    select(sys.argv[1]) 
