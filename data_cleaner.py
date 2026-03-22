import json
import re
import pandas as pd
from sklearn.preprocessing import StandardScaler

gen_freq_dict = {
    "PC3-8500": 1066.0,
    "PC3-10600": 1333.0,
    "PC3-12800": 1600.0,
    "PC3-14900": 1866.0,
    "PC3L-8500": 1066.0,
    "PC3L-10600": 1333.0,
    "PC3L-12800": 1600.0,
    "PC3L-14900": 1866.0,
    "PC4-17000": 2133.0,
    "PC4-19200": 2400.0,
    "PC4-21300": 2666.0,
    "PC4-23400": 2933.0,
    "PC4-25600": 3200.0,
    "PC4-28800": 3600.0,
    "PC5-38400": 4800.0,
    "PC5-44800": 5600.0
}

with open("ram_data.json", "r", encoding='utf-8') as file:
    raw_data = json.load(file)

print(len(raw_data["data"]))

def extract_ram_details(title):

    size = re.search(r'(\d{1,3})\s*(GB)', title, re.IGNORECASE)  #(\d+(?:\.\d+)?)\s*(GB)

    gen = re.search(r'DDR(\d)L*', title, re.IGNORECASE)

    freq_match = re.search(r'(\d{4,5})\s*(MHz|MH|MT/s)', title, re.IGNORECASE) #(\d+(?:\.\d+)?)\s*(MHz|MH|GHz|MT/s)
    freq = None

    if freq_match:
        freq = freq_match.group(1)

    if freq_match is None:
        freq_match = re.search(r'(DDR(\d)L*)[- ]*(\d{4,5})', title, re.IGNORECASE)
        if freq_match:
            freq = float(freq_match.group(3))

    if freq_match is None:
        freq_match = re.search(r'(PC(\d)*L*)[- ]*(\d{4,5})', title, re.IGNORECASE)
        if freq_match:
            freq_type = str(freq_match.group(1)).upper()
            freq_value = str(freq_match.group(3))
            if len(freq_value) == 4 and int(freq_value[0]) < 6:
                freq = freq_value
            else:
                freq_key = f"{freq_type}-{freq_value}"
                freq = gen_freq_dict.get(freq_key)

    brand = re.search(r'(Corsair|G.SKILL|Crucial|TEAMGROUP|Kingston|XPG|Samsung|PNY|Timetec|ADATA|SK Hynix|A-Tech|OWC|Micron|Ballistix|HP|Dell|Patriot Memory|Patriot|Lenovo|QNAP|Adamanta)', title, re.IGNORECASE)

    is_kit = re.search(r'(Kit|((2|3|4|5|6|7|8|9|10|11|12)\s*[xX]\s*(\d{1,3})\s*(GB)))', title, re.IGNORECASE)

    """
    if is_kit is None:
        print(f"is_kit none in: {title}")
        
    if is_kit:
        print(f"kit found in: {title}")
        
    if size is None:
        print(f"size none in: {title}")
    
    if size:
        if float(size.group(1)) > 256:
            print(f"size {float(size.group(1))} in: {title}")
    
    if gen is None:
        print(f"gen none in: {title}")

    if freq is None:
        print(f"freq none in: {title}")
        
    if freq:
        #print(f"freq: {freq}")
        if float(freq) < 1066:
            print(f"freq is {freq} in: {title}")
    """

    return pd.Series([
        float(size.group(1)) if size else None,
        int(gen.group(1)) if gen else None,
        float(freq) if freq else None,
        str(brand.group(1)) if brand else None,
        True if is_kit else False
    ])

def clean_data():
    #print(raw_df.head())
    raw_df = pd.DataFrame(raw_data["data"])
    raw_df[['Capacity_GB', 'Generation', 'Speed_MHz', 'Brand', 'Is_kit']] = raw_df['title'].apply(extract_ram_details)
    raw_df['Final_Price'] = raw_df['price'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
    print(raw_df)

    raw_df = raw_df.drop_duplicates(subset=['asin'])
    raw_df = raw_df.dropna(subset=['asin'])
    raw_df['Brand'] = raw_df['Brand'].fillna("Unknown") #S None 1524
    print(raw_df)

    raw_df = raw_df[(raw_df['Speed_MHz'] >= 1000) & (raw_df['Speed_MHz'] < 10000)]
    raw_df = raw_df[['Capacity_GB', 'Generation', 'Speed_MHz', 'Brand', 'Is_kit', 'Final_Price']]
    clean_df = raw_df.dropna(subset=['Capacity_GB', 'Generation', 'Speed_MHz', 'Brand', 'Is_kit', 'Final_Price'])
    print(clean_df)

    return clean_df

dataset = clean_data()
print(dataset)

with open("ram_data_cleaned.csv", "w", encoding='utf-8') as file:
    dataset.to_csv(file, index=False)

"""
check = []
check_unique = []
check.extend(dataset.Is_kit)
check_unique.extend(dataset.Is_kit.unique())
print(check_unique)
print(check)
"""