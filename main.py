import re
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from data_manipulation.default_values import *

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

def create_data(capacity_gb, generation, speed, latency: list, voltage: list, is_kit, user_data: list):

    for l, v in zip(latency, voltage):
        data = {
            'Capacity_GB': [float(capacity_gb)],
            'Generation': [float(generation)],
            'Speed_MHz': [float(speed)],
            'Latency': [float(l)],
            'Voltage': [float(v)],
            'Is_kit': [int(is_kit)]
        }
        user_data.append(data)

    #print(len(user_data))
    #print(user_data)
    return user_data

def predict_price(capacity_gb, generation, speed, latency, voltage, brand, is_kit):
    try:
        if capacity_gb is None or speed is None:
            raise ValueError('RAM capacity and speed are required')

        if generation is None:
            generation = default_gen(speed, capacity_gb)

        gaming_latency, office_latency = None, None
        if latency is None:
            #print(f"Latency is None")
            gaming_latency = default_cl(generation, speed, True)
            office_latency = default_cl(generation, speed, False)

        gaming_voltage, office_voltage = None, None
        if voltage is None:
            #print(f"Voltage is None")
            gaming_voltage = default_voltage(f"DDR{generation}", True)
            office_voltage = default_voltage(f"DDR{generation}", False)

        if is_kit is None:
            is_kit = 1

        user_data = []
        create_data(
            capacity_gb,
            generation,
            speed,
            [gaming_latency, office_latency] if latency is None else [latency, latency],
            [gaming_voltage, office_voltage] if voltage is None else [voltage, voltage],
            is_kit,
            user_data
        )

        classifier_model, regression_model, classifier_columns, regressor_columns, model_number = None, None, None, None, None

        if 0.0 < user_data[0]['Capacity_GB'][0] <= 128.0:
            ram_class = "!!! PC !!!"
            model_number = 1
        elif 128.0 < user_data[0]['Capacity_GB'][0] <= 768.0:
            ram_class = "!!! ENTERPRICE !!!"
            model_number = 2
        else:
            ram_class = "!!! SERVER MONSTERS !!! \n\n Top price - 27118$ \n (For example 1004+GB capacity gives max price, so predicted price can be much higher depending on what you entered)"
            model_number = 3

        classifier_model = model_sets[model_number][0]
        regressor_model = model_sets[model_number][1]
        classifier_columns = model_sets[model_number][2]
        regressor_columns = model_sets[model_number][3]

        prices = []
        gaming_probs = []
        if gaming_latency is None and office_latency is None and gaming_voltage is None and office_voltage is None:
            values = None
        else:
            values = []

        for data in user_data:
            df = pd.DataFrame(data)

            brand_col = f"Brand_{brand}"
            df[brand_col] = 1

            df_clf = df.reindex(columns=classifier_columns, fill_value=0)

            to_scale = ['Capacity_GB', 'Speed_MHz']
            df_clf[to_scale] = scaler.transform(df_clf[to_scale])

            # predict_proba - vrací pole [[0.51, 0.49]] -> 51% pro Office, 49% pro Gaming
            probs = classifier_model.predict_proba(df_clf)[0]
            gaming_prob = probs[1]
            gaming_probs.append(gaming_prob)
            #print(gaming_prob)

            df_reg = df_clf.copy()
            df_reg['Is_gaming'] = gaming_prob
            df_reg = df_reg.reindex(columns=regressor_columns, fill_value=0)

            prices.append(regressor_model.predict(df_reg)[0])

            if values is not None:
                values.append((data['Latency'], data['Voltage']))

            """
            # graf: co a jak moc ovlivňuje cenu
            importances = regressor_model.feature_importances_  #O kolik sloupec ovlivnil cenu (%)
            features = regressor_columns #Jaký to byl sloupec
            data_imp = pd.Series(importances, index=features).sort_values(ascending=False) #Seřadím od největšího
            data_imp.head(10).plot(kind='barh') #nakreslí graf typu Bar horizontal (barh) s deseti největšími hodnotami
            plt.title("Co nejvíc ovlivňuje cenu?")
            plt.show()
            """

        final_results = print_type_a_price(prices, gaming_probs, values)

        # Odstranění duplicit při zachování pořadí
        unique_results = [ram_class]
        for result in final_results:
            unique_part = re.sub(r"- .+ -", "", result).strip()
            if unique_part not in [re.sub(r"- .+ -", "", u).strip() for u in unique_results]:
                unique_results.append(result)

        return unique_results

    except ValueError as e:
        #print(f"err1: {e}")
        return f"err1: {e}"
    except TypeError as e:
        #print(f"err2: {e}")
        return f"err1: {e}"

def  print_type_a_price(price_estimates, ram_type_probs, values_cl_v):
    results = []

    try:
        index = 0
        for prob in ram_type_probs:
            if 0 <= prob < 0.25:
                ram_type = 'not GAMING'
            elif 0.25 <= prob < 0.45:
                ram_type = 'rather not GAMING'
            elif 0.45 <= prob < 0.55:
                ram_type = 'cannot determine'
            elif 0.55 <= prob < 0.8:
                ram_type = 'rather GAMING'
            else:
                ram_type = 'GAMING'

            if values_cl_v is not None:
                cl, v = values_cl_v[index]
                results.append(f"\n - S{index+1} (latency: {cl}, voltage: {v}) - \n RAM type: {ram_type}, Odhadovaná cena: {price_estimates[index]:.2f}$")
            else:
                results.append(f"\n - S{index + 1} - \n RAM type: {ram_type}, Odhadovaná cena: {price_estimates[index]:.2f}$")
            index += 1

        return results

    except ValueError as e:
        #print(f"err3: {e}")
        return f"err3: {e}"

"""
for i in predict_price(512, 5, 6400, None, None, "NEMIX", 1):
    print(i)
"""