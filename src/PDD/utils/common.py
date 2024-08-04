import os
import pickle
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        for i in range(len(list(models))):

            model = list(models.values())[i]
            model.fit(X_train,y_train)

            y_test_pred = model.predict(X_test)

            test_model_score = accuracy_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score

            return report

    except Exception as e:
        raise e




def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise e
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise e