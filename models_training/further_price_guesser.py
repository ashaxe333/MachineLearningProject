import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

data_path = '../data/ram_data_cleaned_enterprice.csv'
model_name = '../models/regressor_enterprice.pkl',
column_path = '../columns/regressor_cols_enterprice.pkl'

def train_model(path_to_file, path_to_model, path_to_columns):
    data = pd.read_csv(path_to_file, sep=",")

    data = pd.get_dummies(data, columns=['Brand'], drop_first=True)

    input_features = data.drop(['title', 'Final_Price'], axis=1)
    target_feature = data['Final_Price']

    X_train, X_test, y_train, y_test = train_test_split(input_features, target_feature, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    to_scale = ['Capacity_GB', 'Speed_MHz']
    X_train[to_scale] = scaler.fit_transform(X_train[to_scale])
    X_test[to_scale] = scaler.transform(X_test[to_scale])

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(f"mae: {mean_absolute_error(y_test, y_pred)}")
    print(f"mse: {mean_squared_error(y_test, y_pred)}")
    print(f"R2 Score: {r2_score(y_test, y_pred)}")

    joblib.dump(model, path_to_model)
    joblib.dump(X_train.columns.tolist(), path_to_columns)

train_model(data_path, model_name, column_path)