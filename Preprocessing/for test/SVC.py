# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 02:32:19 2021

@author: 이충섭
"""

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np

print('done')

df1 = pd.read_csv('train_8.csv')
df2 = pd.read_csv('validation_8.csv')

print('done1')
 
X_train = df1['Lead']
y_train = df1['Label']
X_test = df2['Lead']
y_test = df2['Label']
 
print('done2')

#%%

print(df1['Subject'][5])

#%%

sc = StandardScaler()
sc.fit(X_train)
 
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
 
 
svm_model = SVC(kernel='rbf', C=8, gamma=0.1)


svm_model.fit(X_train_std, y_train) # SVM 분류 모델 훈련
print('done svc')
 
y_pred = svm_model.predict(X_test_std) # 테스트
 
print("예측된 라벨:", y_pred)
print("ground-truth 라벨:", y_test)
 
print("prediction accuracy: {:.2f}".format(np.mean(y_pred == y_test))) # 예측 정확도