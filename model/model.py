import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from joblib import dump, load
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score
from imblearn.pipeline import Pipeline, make_pipeline
from imblearn.over_sampling import SMOTE
from persist import save_model, load_model


def load_data():
    """
    Return the X and y values from the processed data
    """
    data = pd.read_csv("02_cleaned_data.csv")
    data=data.drop(["Unnamed: 0"], axis=1)
    X = data.drop(["Childlabour_06"], axis=1)
    y = data["Childlabour_06"]

    return X, y

def get_model():
    return LogisticRegression(max_iter = 10000)


def split_data(X, y):
    """
    Split the data into test and train splits
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = 0.2, random_state = 42, stratify = y
    )

    return X_train, X_test, y_train, y_test

smt = SMOTE(random_state=45, sampling_strategy = 1.0)

def train_model(model, X_train_os, y_train_os):
    model.fit(X_train_os, y_train_os)
    y_train_preds=model.predict(X_train_os)
    train_report=confusion_matrix(y_train_os, y_train_preds)
    print("Confusion matrix from training data")
    print(train_report)

def test_model(model, X_test, y_test):
    y_test_preds=model.predict(X_test)
    test_report=confusion_matrix(y_test, y_test_preds)
    print("Confusion matrix from testing data")
    print(test_report)

# X_train_os, y_train_os = smt.fit_sample(X_train, y_train)

# def save_model(model):
#     dump(model, "model.joblib")

# def load_model():
#     return load("model.joblib")




if __name__ == "__main__":
    X, y=load_data()
    X_train, X_test, y_train, y_test= train_test_split(X,y)
    X_train_os, y_train_os= smt.fit_sample(X_train, y_train)
    print("X data")
    print(X)
    print("X_train data")
    print(X_train)
    print("X_train_os data")
    print(X_train_os.shape)

    model=get_model()
    train_model(model, X_train_os, y_train_os)
    save_model(model)
    del model

    loaded_model= load_model()

    test_model(loaded_model, X_test, y_test)


