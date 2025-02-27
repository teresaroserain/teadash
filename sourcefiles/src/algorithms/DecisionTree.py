import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics
import os.path as Path
import os

def splitData(df):
    X_test = df[['ParticipatedDiscussion', 'Posts', 'ParticipatedQuiz']] # Features
    y_test = df[['ParticipateInTarget']] # Target variable
    y_test = y_test.astype('int')

    df_train = pd.read_csv(os.path.join(Path.abspath(Path.join(__file__ ,"../../.."))+'/Datasets/df_train.csv'), delimiter=";")   
    X_train = df_train[['ParticipatedDiscussion', 'Posts', 'ParticipatedQuiz']]
    y_train = df_train[['ParticipateInTarget']]

    # Split dataset into training set and test set
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=100) # 70% training and 30% test
    return X_train, X_test, y_train, y_test 

def buildDecisionTree(df):
    # Create Decision Tree classifer object
    clf = DecisionTreeClassifier()
    X_train, X_test, y_train, y_test  = splitData(df)
    # Train Decision Tree Classifer
    clf = clf.fit(X_train,y_train)

    #Predict the response for test dataset
    y_pred = clf.predict(X_test)
    print("prediction test set ", X_test)
    print("predicted value ", y_pred)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    df = df.assign(PredictedValue=y_pred)
    
    return df, metrics.accuracy_score(y_test, y_pred)

