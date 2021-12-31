# -*- coding: utf-8 -*-
"""Before_ANN_Numeric.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MSX6GQ46o-c2cqqtR8Q_yiyFEEo7lJdS
"""

from google.colab import drive
drive.mount("/content/drive")

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("/content/drive/MyDrive/ML_Results/preprocessed.csv")

X = df.iloc[:, 0:-1].values
Y = df.iloc[:, -1].values


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units = 7,activation='relu'))
ann.add(tf.keras.layers.Dense(units = 1,activation='sigmoid'))
ann.compile(optimizer = 'adam', loss = 'mse', metrics = ['accuracy'])
history = ann.fit(X_train, y_train, epochs = 10, batch_size=32, validation_split = 0.2)

loss, acc = ann.evaluate(X_test, y_test)

print("Loss: ", loss)
print("Accuracy: ", acc)

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, roc_curve, auc, roc_auc_score

y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)

print("Classification report for classifier %s:\n%s\n" % (
    ann, classification_report(y_test, y_pred)))

################# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix")
print(cm)

################ Accuracy
print()
print("Model accuracy: ", accuracy_score(y_test, y_pred))

################### Loss Curve
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training loss', 'Validation loss'], loc='upper right')
plt.show()

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

import pickle
fileName = "/content/drive/MyDrive/ML_Results_Main/ANN_Numeric_Before.model"
pickle.dump(ann, open(fileName, 'wb'))