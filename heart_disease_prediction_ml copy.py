"""
             SCHEMA
1. import libraries
2. load dataset and EDA
3. handling missing value
4. train test split
5. standardization
6. categorical coding
7. modeling: RF, KNN, Voting Classifier train and test
6. CM (confusion matrix)

data source:
https://www.kaggle.com/datasets/redwankarimsony/heart-disease-data
"""

#1. IMPORT LIBRARIES

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import warnings
warnings.filterwarnings("ignore")

#2. LOAD DATASET and EDA

df = pd.read_csv("heart_disease_uci.csv")
df = df.drop(columns=["id"])
df.info()
describe = df.describe()

numerical_features = df.select_dtypes(include=[np.number]).columns.tolist()

plt.figure()
sns.pairplot(df, vars=numerical_features, hue = "num")
plt.show()

plt.figure()
sns.countplot(x="num", data=df)
plt.show()

#3. HANDILNG MISSING VALUE

print(df.isnull().sum())
df = df.drop(columns=["ca"])
print(df.isnull().sum())

df["trestbps"].fillna(df["trestbps"].median(), inplace = True )
df["chol"].fillna(df["chol"].median(), inplace = True )
df["fbs"].fillna(df["fbs"].mode()[0], inplace = True )
df["restecg"].fillna(df["restecg"].mode()[0], inplace = True )
df["thalch"].fillna(df["thalch"].median(), inplace = True )
df["exang"].fillna(df["exang"].mode()[0],inplace = True )
df["oldpeak"].fillna(df["oldpeak"].median(), inplace = True )
df["slope"].fillna(df["slope"].mode()[0], inplace = True )
df["thal"].fillna(df["thal"].mode()[0], inplace = True )

print(df.isnull().sum())

#4. TRAIN TEST SPLIT - STANDARDIZATIN - CATEGORİCAL CODING

X = df.drop(["num"], axis=1)
y = df["num"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

categorical_features = ["sex", "dataset", "cp", "restecg", "exang", "slope", "thal"]
numerical_features = ["age", "trestbps", "chol", "fbs", "thalch", "oldpeak"]

X_train_num = X_train[numerical_features]
X_test_num = X_test[numerical_features]

scaler = StandardScaler()
X_train_num_scaled = scaler.fit_transform(X_train_num)
X_test_num_scaled = scaler.transform(X_test_num)

encoder = OneHotEncoder(handle_unknown='ignore', drop="first", sparse_output=False)
#encoder = OneHotEncoder(sparse=False, drop="first")
X_train_cat = X_train[categorical_features]
X_test_cat = X_test[categorical_features]

X_train_cat_encoded = encoder.fit_transform(X_train_cat)
X_test_cat_encoded = encoder.transform(X_test_cat)

# X_train_transformed = np.hstack((X_train_num_scaled, X_train_cat_encoded.reshape(-1,1)))
# X_test_transformed = np.hstack((X_test_num_scaled, X_test_cat_encoded.reshape(-1,1)))

X_train_transformed = np.hstack((X_train_num_scaled, X_train_cat_encoded))
X_test_transformed = np.hstack((X_test_num_scaled, X_test_cat_encoded))

#7. MODELING: RF,KNN,VOTING CLASSIFIER TRAIN AND TEST

rf = RandomForestClassifier(n_estimators=100, random_state=42)
knn = KNeighborsClassifier()

voting_clf = VotingClassifier(estimators=[
    ("rf",rf),
    ("knn",knn)], voting="soft")

# model training
voting_clf.fit(X_train_transformed, y_train)

# prediction with test data
y_pred = voting_clf.predict(X_test_transformed)

print("Accuracy: ", accuracy_score(y_test, y_pred))
print("Confusion Matrix: ")
cm = confusion_matrix(y_test, y_pred)
print(cm)
print("Classification Report: ")
print(classification_report(y_test, y_pred))

#8. CM

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot = True, fmt="d", cmap="Blues", cbar=False)
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True label")
plt.show()













