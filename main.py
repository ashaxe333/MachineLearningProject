import re
import pandas as pd
import joblib
import matplotlib.pyplot as plt

model_sets = {
    1: [
        joblib.load('models/classifier.pkl'),
        joblib.load('models/regressor.pkl'),
        joblib.load('columns/classifier_cols.pkl'),
        joblib.load('columns/regressor_cols.pkl')
    ],
}

classifier = joblib.load('models/classifier.pkl')
regressor = joblib.load('models/regressor.pkl')
classifier_cols = joblib.load('columns/classifier_cols.pkl')
regressor_cols = joblib.load('columns/regressor_cols.pkl')

#all
classifier_all = joblib.load('models/classifier_all.pkl')
regressor_all = joblib.load('models/regressor_all.pkl')
classifier_cols_all = joblib.load('columns/classifier_cols_all.pkl')
regressor_cols_all = joblib.load('columns/regressor_cols_all.pkl')

classifier_PC = joblib.load('models/classifier_PC.pkl')
regressor_PC = joblib.load('models/regressor_PC.pkl')
classifier_cols_PC = joblib.load('columns/classifier_cols_PC.pkl')
regressor_cols_PC = joblib.load('columns/regressor_cols_PC.pkl')

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

        classifier_model, regression_model, classifier_columns, regressor_columns = None, None, None, None

        if user_data['Capacity_GB'][0] <= 128.0:
            print("!!! PC !!!")
            classifier_model = classifier_PC
            regressor_model = regressor_PC
            classifier_columns = classifier_cols_PC
            regressor_columns = regressor_cols_PC
        elif 128.0 < user_data['Capacity_GB'][0] <= 768.0:
            print("!!! ENTERPRICE !!!")
            classifier_model = classifier
            regressor_model = regressor
            classifier_columns = classifier_cols
            regressor_columns = regressor_cols
        else:
            print("!!! MONSTERS !!!")
            classifier_model = classifier_all
            regressor_model = regressor_all
            classifier_columns = regressor_cols_all
            regressor_columns = regressor_cols_all

        df = pd.DataFrame(user_data)

        # 2. Vyřešení Brandu (One-Hot Encoding)
        # Vytvoříme sloupec s vybranou značkou
        brand_col = f"Brand_{brand}"
        df[brand_col] = 1

        # TEĎ TA MAGIE: Doplníme všechny ostatní Brand_ nuly, které model čeká
        # reindex zajistí, že df bude mít PŘESNĚ ty sloupce co columns_classifier a ve správném pořadí
        df_clf = df.reindex(columns=classifier_columns, fill_value=0)

        # 3. Scaling (pouze pro numerické hodnoty)
        to_scale = ['Capacity_GB', 'Speed_MHz']
        df_clf[to_scale] = scaler.transform(df_clf[to_scale])

        """
        # 4. Predikce Is_gaming (Krok 1)
        # Použijeme tvůj nápad s pravděpodobností (pokud chceš být profík)
        # is_gaming_prob = classifier.predict_proba(df_clf)[0][1]
        is_gaming = classifier_model.predict(df_clf)[0]

        # 5. Příprava pro Regresor (Krok 2)
        # Regresor má možná jiné sloupce (třeba tam má Is_gaming navíc)
        df_reg = df_clf.copy()
        df_reg['Is_gaming'] = is_gaming
        """

        # 4. Predikce Is_gaming (Krok 1) - Místo predict použijeme predict_proba
        # predict_proba vrací např. [[0.51, 0.49]] -> 51% pro Office, 49% pro Gaming
        probs = classifier_model.predict_proba(df_clf)[0]
        gaming_prob = probs[1]  # To je ta pravděpodobnost pro "Herní" (třída 1)

        # Teď už nemusíš vracet jen 0/1, ale přímo tohle číslo
        is_gaming = 1 if gaming_prob > 0.5 else 0
        print(gaming_prob)

        # 5. Predikce Ceny (Krok 2)
        df_reg = df_clf.copy()

        # Tady je trik: Do regresoru pošli tu spojitou pravděpodobnost (např. 0.49)!
        # Regresor s tím umí pracovat lépe než s natvrdo hozenou nulou.
        df_reg['Is_gaming'] = gaming_prob
        # Opět reindex, aby sloupce seděly s regresorem
        df_reg = df_reg.reindex(columns=regressor_columns, fill_value=0)

        price = regressor_model.predict(df_reg)[0]

        # co a jak moc ovlivňuje cenu
        importances = regressor_model.feature_importances_
        features = regressor_columns
        data_imp = pd.Series(importances, index=features).sort_values(ascending=False)

        data_imp.head(10).plot(kind='barh')
        plt.title("Co nejvíc ovlivňuje cenu?")
        plt.show()

        return price, gaming_prob

    except ValueError as e:
        print(f"err: {e}")
        return None, None


price_estimate, ram_type_prob = predict_price(1536, 5, 6400, 52, 1.25, "-", 1)
ram_type = None
if 0 <= ram_type_prob < 0.25:
    ram_type = 'OFFICE'
elif 0.3 <= ram_type_prob < 0.45:
    ram_type = 'rather OFFICE'
elif 0.45 <= ram_type_prob < 0.55:
    ram_type = 'cannot determine'
elif 0.55 <= ram_type_prob < 0.8:
    ram_type = 'rather GAMING'
else:
    ram_type = 'GAMING'

print(f"RAM type: {ram_type}, Odhadovaná cena: {price_estimate:.2f} $")