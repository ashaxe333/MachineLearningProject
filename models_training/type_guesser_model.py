import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

data_paths = [
    '../data/ram_data_cleaned.csv',
    '../data/ram_data_cleaned_all.csv',
    '../data/ram_data_cleaned_PC.csv'
]

model_names = [
    '../models/classifier.pkl',
    '../models/classifier_all.pkl',
    '../models/classifier_PC.pkl'
]

column_paths = [
    '../columns/classifier_cols.pkl',
    '../columns/classifier_cols_all.pkl',
    '../columns/classifier_cols_PC.pkl'
]

def train_model(path_to_file, path_to_model, path_to_columns):
    """
    Trains classifier model and saves it in a pickle file.
    :param path_to_file: path to file to be trained
    :param path_to_model: path to model to be saved
    """
    data = pd.read_csv(path_to_file, sep=",")

    data = pd.get_dummies(data, columns=['Brand'], drop_first=True)

    input_features = data.drop(['title', 'Final_Price', 'Is_gaming'], axis=1)
    target_feature = data['Is_gaming']

    X_train, X_test, y_train, y_test = train_test_split(input_features, target_feature, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    to_scale = ['Capacity_GB', 'Speed_MHz']
    X_train[to_scale] = scaler.fit_transform(X_train[to_scale])
    X_test[to_scale] = scaler.transform(X_test[to_scale])

    model = RandomForestClassifier(max_depth=100, n_estimators=200, class_weight='balanced', min_samples_split=4, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nDetailed Report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, path_to_model)
    joblib.dump(X_train.columns.tolist(), path_to_columns)

    """
    once = True
    while once:
        joblib.dump(scaler, '../columns/scaler.pkl')
        once = False
    """

train_model(data_paths[2], model_names[2], column_paths[2])

"""
index = 0
while index < len(model_names):
    train_model(data_paths[index], model_names[index], column_paths[index])
    index += 1
"""