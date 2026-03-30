import re
import pandas as pd
import joblib
import matplotlib.pyplot as plt

model_sets = {
    1: [
        joblib.load('models/classifier_PC.pkl'),
        joblib.load('models/regressor_PC.pkl'),
        joblib.load('columns/classifier_cols_PC.pkl'),
        joblib.load('columns/regressor_cols_PC.pkl')
    ],
    2: [
        joblib.load('models/classifier.pkl'),
        joblib.load('models/regressor.pkl'),
        joblib.load('columns/classifier_cols.pkl'),
        joblib.load('columns/regressor_cols.pkl')
    ],
    3: [
        joblib.load('models/classifier_all.pkl'),
        joblib.load('models/regressor_all.pkl'),
        joblib.load('columns/classifier_cols_all.pkl'),
        joblib.load('columns/regressor_cols_all.pkl')
    ]
}

scaler = joblib.load('columns/scaler.pkl')

def predict_price(capacity_gb, generation, speed, latency, voltage, brand, is_kit):
    try:
        # 1. Vytvoření základního slovníku (bez Brandu pro One-Hot)
        user_data = {
            'Capacity_GB': [float(capacity_gb)],
            'Generation': [float(generation)],
            'Speed_MHz': [float(speed)],
            'Latency': [float(latency)],
            'Voltage': [float(voltage)],
            'Is_kit': [int(is_kit)]
        }

        classifier_model, regression_model, classifier_columns, regressor_columns, model_number = None, None, None, None, None

        if 0.0 < user_data['Capacity_GB'][0] <= 128.0:
            print("!!! PC !!!")
            model_number = 1
        elif 128.0 < user_data['Capacity_GB'][0] <= 768.0:
            print("!!! ENTERPRICE !!!")
            model_number = 2
        else:
            print("!!! SERVER MONSTERS !!!")
            print("Top price - 27 118$ \n (For example 1004+GB capacity gives max price, so predicted price can be much higher depending on what you entered)")
            model_number = 3

        classifier_model = model_sets[model_number][0]
        regressor_model = model_sets[model_number][1]
        classifier_columns = model_sets[model_number][2]
        regressor_columns = model_sets[model_number][3]

        df = pd.DataFrame(user_data)

        # 2. Vyřešení Brandu (One-Hot Encoding)
        # Vytvoříme sloupec s vybranou značkou
        brand_col = f"Brand_{brand}"
        df[brand_col] = 1

        # reindex zajistí, že df bude mít přesně ve správněm pořadí ty sloupce co columns_classifier
        df_clf = df.reindex(columns=classifier_columns, fill_value=0)

        # 3. Scaling (musím i zde, protože je na tom model naučený)
        to_scale = ['Capacity_GB', 'Speed_MHz']
        df_clf[to_scale] = scaler.transform(df_clf[to_scale])

        # 4. predict_proba - vrací pole [[0.51, 0.49]] -> 51% pro Office, 49% pro Gaming
        probs = classifier_model.predict_proba(df_clf)[0]
        gaming_prob = probs[1]
        print(gaming_prob)

        # 5. Predikce Ceny (Krok 2)
        df_reg = df_clf.copy()
        df_reg['Is_gaming'] = gaming_prob
        df_reg = df_reg.reindex(columns=regressor_columns, fill_value=0)

        price = regressor_model.predict(df_reg)[0]

        """
        # graf: co a jak moc ovlivňuje cenu
        importances = regressor_model.feature_importances_  #O kolik sloupec ovlivnil cenu (%)
        features = regressor_columns #Jaký to hbyl sloupec
        data_imp = pd.Series(importances, index=features).sort_values(ascending=False) #Seřadím od největšího
        data_imp.head(10).plot(kind='barh') #nakreslí graf typu Bar horizontal (barh) s deseti největšími hodnotami
        plt.title("Co nejvíc ovlivňuje cenu?")
        plt.show()
        """

        return price, gaming_prob

    except ValueError as e:
        print(f"err: {e}")
        return None, None


price_estimate, ram_type_prob = predict_price(960, 5, 6400, 52, 1.1, "NEMIX", 1)
ram_type = None
if 0 <= ram_type_prob < 0.25:
    ram_type = 'not GAMING'
elif 0.25 <= ram_type_prob < 0.45:
    ram_type = 'rather not GAMING'
elif 0.45 <= ram_type_prob < 0.55:
    ram_type = 'cannot determine'
elif 0.55 <= ram_type_prob < 0.8:
    ram_type = 'rather GAMING'
else:
    ram_type = 'GAMING'

print(f"RAM type: {ram_type}, Odhadovaná cena: {price_estimate:.2f} $")