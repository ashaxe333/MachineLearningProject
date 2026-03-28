import re
import pandas as pd
import joblib

classifier = joblib.load('models/gaming_classifier.pkl')
regressor = joblib.load('models/price_regressor.pkl')
columns_classifier = joblib.load('columns/gaming_classifier_columns.pkl')
columns_regressor = joblib.load('columns/price_regressor_columns.pkl')

#all
classifier_all = joblib.load('models/gaming_classifier_all.pkl')
regressor_all = joblib.load('models/price_regressor_all.pkl')
columns_classifier_all = joblib.load('columns/gaming_classifier_all_columns.pkl')
columns_regressor_all = joblib.load('columns/price_regressor_all_columns.pkl')

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

        df = pd.DataFrame(user_data)

        # 2. Vyřešení Brandu (One-Hot Encoding)
        # Vytvoříme sloupec s vybranou značkou
        brand_col = f"Brand_{brand}"
        df[brand_col] = 1

        # TEĎ TA MAGIE: Doplníme všechny ostatní Brand_ nuly, které model čeká
        # reindex zajistí, že df bude mít PŘESNĚ ty sloupce co columns_classifier a ve správném pořadí
        df_clf = df.reindex(columns=columns_classifier, fill_value=0)

        # 3. Scaling (pouze pro numerické hodnoty)
        to_scale = ['Capacity_GB', 'Speed_MHz']
        df_clf[to_scale] = scaler.transform(df_clf[to_scale])

        # 4. Predikce Is_gaming (Krok 1)
        # Použijeme tvůj nápad s pravděpodobností (pokud chceš být profík)
        # is_gaming_prob = classifier.predict_proba(df_clf)[0][1]
        is_gaming = classifier.predict(df_clf)[0]

        # 5. Příprava pro Regresor (Krok 2)
        # Regresor má možná jiné sloupce (třeba tam má Is_gaming navíc)
        df_reg = df_clf.copy()
        df_reg['Is_gaming'] = is_gaming

        # Opět reindex, aby sloupce seděly s regresorem
        df_reg = df_reg.reindex(columns=columns_regressor, fill_value=0)

        price = regressor.predict(df_reg)[0]

        return price, is_gaming

    except ValueError as e:
        print(f"err: {e}")

odhad_ceny, typ_ram = predict_price(32, 5, 3200, 36, 1.35, "Corsair", 1)
print(f"Typ: {'Herní' if typ_ram else 'Kancelářská'}, Odhadovaná cena: {odhad_ceny:.2f} $")