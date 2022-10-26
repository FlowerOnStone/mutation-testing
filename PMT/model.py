from __future__ import division, print_function, unicode_literals
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import sklearn.model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import os


mutationOperatorDictionary = ["AOD", "AOR", "ASR", "BCR", "COD", "COI", "CRP", "DDL", "EHD", "EXS", "IHD", "IOD", "IOP",
                              "LCR", "LOD", "LOR", "ROR", "SCD", "SCI", "SIR"]
typeStatementDictionary = ["conditional", "assignment", "return", "loop", "method", "unknow"]
typeReturnDictionary = ["float", "matrix", "int", "bool", "Unknown"]
resultDictionary = ["killed", "survived"]

filenames = os.listdir('./')
filenames = [filename for filename in filenames if ".csv" in filename]

report = {
    "filename": [],
    "numMutant": [],
    "killed": [],
    "survived": [],
    "LogisticRegression_accuracy_score": [],
    "LogisticRegression_f1_score": [],
    "LogisticRegression_predict_killed": [],
    "LogisticRegression_predict_survived": [],
    "LogisticRegression_match_killed": [],
    "LogisticRegression_match_survived": [],
    "RandomForestClassifier_accuracy_score": [],
    "RandomForestClassifier_f1_score": [],
    "RandomForestClassifier_predict_killed": [],
    "RandomForestClassifier_predict_survived": [],
    "RandomForestClassifier_match_killed": [],
    "RandomForestClassifier_match_survived": [],
}



def classifier(filename):
    data = pd.read_csv(filename)
    features = ["distanceBetweenTwoMutant"]
    for i in range(1, 3):
        features.append("mutant" + str(i) + "DepthOnAST")
        feature = "mutant" + str(i) + "TypeOperator"
        for typeOperator in mutationOperatorDictionary:
            subFeature = feature + typeOperator
            data[subFeature] = 0
            data.loc[data[feature] == typeOperator, subFeature] = 1
            features.append(subFeature)
        feature = "mutant" + str(i) + "TypeStatement"
        for typeStatement in typeStatementDictionary:
            subFeature = feature + typeStatement
            data[subFeature] = 0
            data.loc[data[feature] == typeStatement, subFeature] = 1
            features.append(subFeature)
        feature = "mutant" + str(i) + "TypeReturn"
        for typeReturn in typeReturnDictionary:
            subFeature = feature + typeReturn
            data[subFeature] = 0
            data.loc[data[feature] == typeReturn, subFeature] = 1
            features.append(subFeature)

    report["filename"].append(filename)
    report["numMutant"].append(len(data["result"]))
    resultStatus = data["result"].value_counts()
    for status in resultDictionary:
        if status in resultStatus:
            report[status].append(resultStatus[status])
        else:
            report[status].append(0)

    data.loc[data["result"] != "survived", "result"] = 0
    data.loc[data["result"] == "survived", "result"] = 1
    data["result"] = data["result"].astype(int)

    X = data[features]
    y = data.result
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)
    logreg = LogisticRegression(max_iter=2000)
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)

    report["LogisticRegression_accuracy_score"].append(accuracy_score(y_test, y_pred))
    report["LogisticRegression_f1_score"].append(f1_score(y_test, y_pred))
    predict_survived = 0
    predict_killed = 0
    match_survived = 0
    match_killed = 0
    tmp = list(y_test)
    print(filename)
    for i in range(len(y_pred)):
        if y_pred[i] == 1:
            predict_survived += 1
            if tmp[i] == 1:
                match_survived += 1
        else:
            predict_killed += 1
            if tmp[i] == 0:
                match_killed += 1
    report["LogisticRegression_predict_survived"].append(predict_survived / len(y_test))
    report["LogisticRegression_predict_killed"].append(predict_killed / len(y_test))
    report["LogisticRegression_match_survived"].append(match_survived / y_test.value_counts()[1])
    report["LogisticRegression_match_killed"].append(match_killed / y_test.value_counts()[0])
    rfc = RandomForestClassifier()
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)
    report["RandomForestClassifier_accuracy_score"].append(accuracy_score(y_test, y_pred))
    report["RandomForestClassifier_f1_score"].append(f1_score(y_test, y_pred))
    predict_survived = 0
    predict_killed = 0
    match_survived = 0
    match_killed = 0
    for i in range(len(y_pred)):
        if y_pred[i] == 1:
            predict_survived += 1
            if tmp[i] == 1:
                match_survived += 1
        else:
            predict_killed += 1
            if tmp[i] == 0:
                match_killed += 1
    report["RandomForestClassifier_predict_survived"].append(predict_survived / len(y_test))
    report["RandomForestClassifier_predict_killed"].append(predict_killed / len(y_test))
    report["RandomForestClassifier_match_survived"].append(match_survived / y_test.value_counts()[1])
    report["RandomForestClassifier_match_killed"].append(match_killed / y_test.value_counts()[0])

for filename in filenames:
    if filename != 'report.csv':
        classifier(filename)

report = pd.DataFrame(report)
report.to_csv("report.csv", index=False)