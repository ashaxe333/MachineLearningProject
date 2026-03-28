import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

data = pd.read_csv("../data/ram_data_cleaned_all.csv", sep=",")

data = pd.get_dummies(data, columns=['Brand'], drop_first=True)

input_features = data.drop(['title', 'Final_Price', 'Is_gaming'], axis=1)
target_feature = data['Is_gaming']

X_train, X_test, y_train, y_test = train_test_split(input_features, target_feature, test_size=0.3)

scaler = StandardScaler()
to_scale = ['Capacity_GB', 'Speed_MHz']
X_train[to_scale] = scaler.fit_transform(X_train[to_scale])
X_test[to_scale] = scaler.transform(X_test[to_scale])

model = RandomForestClassifier(max_depth=100, n_estimators=200, class_weight='balanced', min_samples_split=5, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Accuracy (Přesnost): {accuracy_score(y_test, y_pred):.2f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nDetailed Report:")
print(classification_report(y_test, y_pred))

joblib.dump(model, '../models/gaming_classifier_all.pkl')