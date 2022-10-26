from __future__ import division, print_function, unicode_literals
import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LogisticRegression


def get_title(name):
    title_search = re.search(' ([A-Za-z]+)\.', name)
    if title_search:
        return title_search.group(1)
    return ""

Title_Dictionary = {
                        "Capt":       "Officer",
                        "Col":        "Officer",
                        "Major":      "Officer",
                        "Jonkheer":   "Royal",
                        "Don":        "Royal",
                        "Sir" :       "Royal",
                        "Dr":         "Officer",
                        "Rev":        "Officer",
                        "Countess":   "Royal",
                        "Dona":       "Royal",
                        "Mme":        "Mrs",
                        "Mlle":       "Miss",
                        "Ms":         "Mrs",
                        "Mr" :        "Mr",
                        "Mrs" :       "Mrs",
                        "Miss" :      "Miss",
                        "Master" :    "Master",
                        "Lady" :      "Royal"
                        }

def titlemap(x):
    return Title_Dictionary[x]


def fillAges(row):
    if not (np.isnan(row['Age'])):
        return row['Age']

    if row['Sex'] == 'female' and row['Pclass'] == 1:
        if row['Title'] == 'Miss':
            return 30
        elif row['Title'] == 'Mrs':
            return 45
        elif row['Title'] == 'Officer':
            return 49
        elif row['Title'] == 'Royalty':
            return 39

    elif row['Sex'] == 'female' and row['Pclass'] == 2:
        if row['Title'] == 'Miss':
            return 20
        elif row['Title'] == 'Mrs':
            return 30

    elif row['Sex'] == 'female' and row['Pclass'] == 3:
        if row['Title'] == 'Miss':
            return 18
        elif row['Title'] == 'Mrs':
            return 31

    elif row['Sex'] == 'male' and row['Pclass'] == 1:
        if row['Title'] == 'Master':
            return 6
        elif row['Title'] == 'Mr':
            return 41.5
        elif row['Title'] == 'Officer':
            return 52
        elif row['Title'] == 'Royalty':
            return 40

    elif row['Sex'] == 'male' and row['Pclass'] == 2:
        if row['Title'] == 'Master':
            return 2
        elif row['Title'] == 'Mr':
            return 30
        elif row['Title'] == 'Officer':
            return 41.5

    elif row['Sex'] == 'male' and row['Pclass'] == 3:
        if row['Title'] == 'Master':
            return 6
        elif row['Title'] == 'Mr':
            return 26

def isRare(title):
    if title == "Mr" or title == "Mrs" or title == "Master" or title == "Miss":
        return 0
    return 1


def loadTitanicData(filename):
    data = pd.read_csv(filename)
    data.drop(["Cabin"], axis=1, inplace=True)
    data["Title"] = data["Name"].apply(get_title)
    data["Title"] = data["Title"].apply(titlemap)
    data["Age"] = data.apply(fillAges, axis=1)
    data["Fare"] = data["Fare"].replace(np.nan, 7.78)
    data["Title"] = data["Title"].apply(isRare)
    data["Family"] = data["Parch"] + data["SibSp"]
    data["Child"] = 0
    data.loc[data["Age"] <= 18, "Child"] = 1
    data.loc[data["Sex"] == "male", "Sex"] = 0  # set male to 0 and female to 1
    data.loc[data["Sex"] == "female", "Sex"] = 1
    data["Sex"] = data["Sex"].astype(int)
    data["Q"] = 0
    data.loc[data["Embarked"] == "Q", "Q"] = 1
    data["S"] = 0
    data.loc[data["Embarked"] == "S", "S"] = 1

    return data


pima = loadTitanicData("train.csv")

feature_cols = ["Q", "S", "Fare", "Pclass", "Age", "Sex", "Family", "Title", "Child"]
X_train = pima[feature_cols]
y_train = pima.Survived


# instantiate the model (using the default parameters)
logreg = LogisticRegression(max_iter=1000)

# fit the model with data
logreg.fit(X_train, y_train)


pima = loadTitanicData("test.csv")

X_test = pima[feature_cols]

results = logreg.predict(X_test)
submission = pd.DataFrame({"PassengerId": pima["PassengerId"], "Survived": results})
submission.to_csv("submission.csv", index=False)