import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

data_paths = [
    "../data/ram_data_cleaned.csv",
    "../data/ram_data_cleaned_cl_None.csv",
    "../data/ram_data_cleaned_cl_default.csv",
    "../data/ram_data_cleaned_brand_unknown.csv",
    "../data/ram_data_cleaned_wo_voltage.csv",
    "../data/ram_data_cleaned_all.csv",
    "../data/ram_data_cleaned_PC.csv"
]

model_names = [
    '../models/regressor.pkl',
    '../models/regressor_cl_None.pkl',
    '../models/regressor_cl_default.pkl',
    '../models/regressor_brand_unknown.pkl',
    '../models/regressor_wo_voltage.pkl',
    '../models/regressor_all.pkl',
    '../models/regressor_PC.pkl'
]

column_paths = [
    '../columns/regressor_cols.pkl',
    '../columns/regressor_cols_cl_None.pkl',
    '../columns/regressor_cols_cl_default.pkl',
    '../columns/regressor_cols_brand_unknown.pkl',
    '../columns/regressor_cols_wo_voltage.pkl',
    '../columns/regressor_cols_all.pkl',
    '../columns/regressor_cols_PC.pkl'
]

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

    model = RandomForestRegressor(max_depth=100, n_estimators=200, min_samples_split=4, criterion='squared_error', random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(f"mae: {mean_absolute_error(y_test, y_pred)}")
    print(f"mse: {mean_squared_error(y_test, y_pred)}")
    print(f"R2 Score: {r2_score(y_test, y_pred)}")

    joblib.dump(model, path_to_model)
    joblib.dump(X_train.columns.tolist(), path_to_columns)

train_model(data_paths[6], model_names[6], column_paths[6])

"""
index = 0
while index < len(model_names):
    train_model(data_paths[index], model_names[index], column_paths[index])
    index += 1
"""