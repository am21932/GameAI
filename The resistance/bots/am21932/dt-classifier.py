import pandas as pd
import numpy as np

#Load CSV files for Bots datasets:
inputs_train=pd.read_csv('datasets/BotsData-train.csv',usecols = [0,1,2,3,4],skiprows = 1,header=None).values
labels_train = pd.read_csv('datasets/BotsData-train.csv',usecols = [5],skiprows = 1 ,header=None).values.reshape(-1,1)
inputs_val=pd.read_csv('datasets/BotsData-test.csv',usecols = [0,1,2,3,4],skiprows = 1,header=None).values
labels_val = pd.read_csv('datasets/BotsData-test.csv',usecols = [5],skiprows = 1 ,header=None).values.reshape(-1,1)


from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import preprocessing

oe = preprocessing.OrdinalEncoder()
inputs_train = oe.fit_transform(inputs_train)
inputs_val = oe.fit_transform(inputs_val)
labels_train = oe.fit_transform(labels_train)
labels_val = oe.fit_transform(labels_val)
    


clf=tree.DecisionTreeClassifier(max_depth=7,min_samples_leaf=1)
clf.fit(inputs_train,labels_train)
output_predictions=clf.predict(inputs_val)
print("output_predictions ",output_predictions)
print("Accuracy ",accuracy_score(labels_val,output_predictions))

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(90,90))
tree.plot_tree(clf, feature_names=['Turn','IsLogicaltonSuspect','IsTrickertonSuspect','IsBounderSuspect','IsSimpletonSuspect'], class_names=['Logicalton','Simpleton','Bounder','Trickerton'],filled=True);
fig.savefig("decision-tree.png")


