import json
import re
import pandas as pd

""" 
        Převod špatně uložených dat - ZMIZÍ
"""
"""
data = {}

with open("ram_data_page1.json", "r", encoding='utf-8') as file:
    data = json.load(file)

#print(data)
print(type(data["data"][0][0]))
data0 = data["data"][0]
data1 = data["data"][1]
data2 = data["data"][2]
data3 = data["data"][3]

data2 = []
for datas in [data0, data1, data2, data3]:
    data2.extend(datas)

final_data = {
    "data": data2
}

print(final_data)

with open('ram_data_page2.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)
"""
"""
        KONEC
"""

with open("ram_data_TEST.json", "r", encoding='utf-8') as file:
    raw_data = json.load(file)

print(len(raw_data["data"]))

df = pd.DataFrame(raw_data["data"])

def extract_ram_details(title):

    size = re.search(r'(\d+)\s*GB', title, re.IGNORECASE)
    gen = re.search(r'DDR(\d)', title, re.IGNORECASE)
    freq = re.search(r'(\d+)\s*MHz', title, re.IGNORECASE)

    return pd.Series([
        int(size.group(1)) if size else None,
        int(gen.group(1)) if gen else None,
        int(freq.group(1)) if freq else None
    ])

#print(df["prices"][31][0]["value"])
df[['Capacity_GB', 'Generation', 'Speed_MHz']] = df['title'].apply(extract_ram_details)
df['Final_Price'] = df['price'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
df = df.drop_duplicates(subset=['asin'])
print(df)
df_clean = df.dropna(subset=['Capacity_GB', 'Generation', 'Speed_MHz', 'Final_Price'])

#print(df_clean.head())
print(df_clean)