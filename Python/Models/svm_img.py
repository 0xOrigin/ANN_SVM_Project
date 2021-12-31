# -*- coding: utf-8 -*-
"""SVM_Img_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1olAb_rt9dy8Pe_GcmYSptdW7kqO0tMla
"""

from google.colab import drive
drive.mount("/content/drive")

import numpy as np
import tensorflow as tf
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import pickle

pickle_in=open('/content/drive/MyDrive/ML_Results_Main/X_SVM_Img_Pre.pickle','rb')
X = np.array(pickle.load(pickle_in))
pickle_in.close()

pickle_in=open('/content/drive/MyDrive/ML_Results_Main/Preprocessing/Y_SVM_Img_Pre.pickle','rb')
Y = np.array(pickle.load(pickle_in))
pickle_in.close()

print("Number of images in dataset: " ,len(X))

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=4)

X = 0  # To solve memory issue

image_size = X_train.shape[1]
input_size = image_size
print("Number of features in image: ", input_size)

X_train=np.reshape(X_train, [-1,input_size])
X_train=X_train.astype('float32')/255

X_test=np.reshape(X_test, [-1,input_size])
X_test=X_test.astype('float32')/255

svm = SVC(C = 10, kernel = 'linear')
svm.fit(X_train, y_train)

accuracy = svm.score(X_test, y_test)

print("Model Accuracy: ", accuracy*100,'%')

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, roc_curve, auc, roc_auc_score

y_pred = svm.predict(X_test)

print("Classification report for classifier %s:\n%s\n" % (
    svm, classification_report(y_test, y_pred)))

################# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix")
print(cm)

################ Accuracy
print()
print("Model accuracy: ", accuracy_score(y_test, y_pred))

from mlxtend.plotting import plot_learning_curves
plot_learning_curves(X_train, y_train, X_test, y_test, svm)

################## ROC Curve
y_pred = y_pred.ravel()
fpr, tpr, _ = roc_curve(y_test,  y_pred)
plt.plot(fpr,tpr)
auc = roc_auc_score(y_test, y_pred)
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.title('ROC Curve')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.show()

fileName = "/content/drive/MyDrive/ML_Results_Main/SVM_Img_78.03.model"
pickle.dump(svm, open(fileName, 'wb'))