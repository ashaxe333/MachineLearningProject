import json
import re
import pandas as pd
import matplotlib.pyplot as plt
from default_values import default_cl, default_voltage

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

with open("../data/ram_data.json", "r", encoding='utf-8') as file:
    raw_data = json.load(file)

print(len(raw_data["data"]))

def extract_ram_details(title):
    """
    Method to extract ram details from product title
    :param title: title of product
    :return: pd.Series with ram details
    """

    is_kit_match = re.search(r'\b(Kit|((\d{1,2})\s*[xX]\s*(\d{1,3})\s*(GB)))\b', title, re.IGNORECASE)
    is_kit = 0
    size = None

    if is_kit_match:
        is_kit = 1
        if is_kit_match.group(3) and is_kit_match.group(4):
            size = int(is_kit_match.group(3)) * int(is_kit_match.group(4))
            if int(is_kit_match.group(3)) == 1:
                is_kit = 0

    if size is None:
        size_match = re.search(r'\b(\d{1,3})\s*(GB)\b', title, re.IGNORECASE)
        if size_match:
            size = int(size_match.group(1))

    gen = re.search(r'\b(DDR(\d)L*)\b', title, re.IGNORECASE)

    freq_match = re.search(r'\b(\d{4,5})\s*(MHz|MH|MT/s)\b', title, re.IGNORECASE) #(\d+(?:\.\d+)?)\s*(MHz|MH|GHz|MT/s)
    freq = None

    if freq_match:
        freq = freq_match.group(1)

    if freq_match is None:
        freq_match = re.search(r'\b(DDR(\d)L*)[- ]*(\d{4,5})\b', title, re.IGNORECASE)
        if freq_match:
            freq = float(freq_match.group(3))

    if freq_match is None:
        freq_match = re.search(r'\b(PC(\d)*L*)[- ]*(\d{4,5})\b', title, re.IGNORECASE)
        if freq_match:
            freq_type = str(freq_match.group(1)).upper()
            freq_value = str(freq_match.group(3))
            if len(freq_value) == 4 and int(freq_value[0]) < 6:
                freq = freq_value
            else:
                freq_key = f"{freq_type}-{freq_value}"
                freq = gen_freq_dict.get(freq_key)
    #_PC
    brand = re.search(r'\b(Acer|Corsair|G.SKILL|Crucial|TEAMGROUP|Kingston|XPG|Samsung|PNY|Timetec|ADATA|SK Hynix|A-Tech|Micron|Ballistix|HP|Patriot Memory|Patriot|Lenovo|QNAP|Adamanta)\b', title, re.IGNORECASE) #servery: |OWC|Dell|NEMIX   #kazí_model:|Acclamator|PUSKILL|GIGASTONE
    #_all
    #brand = re.search(r'\b(Acer|Corsair|G.SKILL|Crucial|TEAMGROUP|Kingston|XPG|Samsung|PNY|Timetec|ADATA|SK Hynix|A-Tech|Micron|Ballistix|HP|Patriot Memory|Patriot|Lenovo|QNAP|Adamanta|OWC|Dell|NEMIX|Acclamator|PUSKILL|GIGASTONE)\b', title, re.IGNORECASE)

    #_enterprice
    #brand = re.search(r'\b(Samsung|SK Hynix|Micron|NEMIX|Adamanta|OWC|Dell|HP|Lenovo|QNAP|Timetec|A-Tech)\b', title, re.IGNORECASE)
    #_gaming
    #brand = re.search(r'\b(Corsair|G.SKILL|XPG|Patriot|TEAMGROUP|ADATA|Ballistix|GIGASTONE|PUSKILL)\b', title, re.IGNORECASE)

    is_gaming = re.search(r'\b(Gaming|RGB|LED|ARGB|Heatsink|Heat\s*Spreader|Overclock|OC|Fury|Vengeance|Trident|Ripjaws|Dominator|Beast|Renegade|Viper|Ballistix|T-Force|XPG)\b', title, re.IGNORECASE) #|CL14|CL16

    latency_match = re.search(r'\b(CL)\s*(\d{1,2})\b', title, re.IGNORECASE)
    latency = None
    if latency_match:
        latency = latency_match.group(2)
    else:
        if freq is None or gen is None:
            latency = None
        else:
            latency = default_cl(int(gen.group(2)), float(freq), True if is_gaming else False)

    voltage_match = re.search(r'\b(\d+(?:\.\d+)?)V\b', title, re.IGNORECASE)
    voltage = None
    if voltage_match:
        voltage = voltage_match.group(1)
    else:
        if gen is None:
            voltage = None
        else:
            voltage = default_voltage(gen.group(1), True if is_gaming else False)


    """
    if is_kit_match is None:
        print(f"is_kit_match none in: {title}")
        
    if is_kit_match:
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
        int(size) if size else None,
        int(gen.group(2)) if gen else None,
        float(freq) if freq else None,
        float(latency) if latency else None,
        float(voltage) if voltage else None,
        str(brand.group(1)).lower() if brand else None,
        int(is_kit),
        1 if is_gaming else 0
    ])

def clean_data():
    """
    Cleans extracted ram data
    :return: cleaned dataset
    """
    #print(raw_df.head())
    raw_df = pd.DataFrame(raw_data["data"])
    raw_df[['Capacity_GB', 'Generation', 'Speed_MHz', 'Latency', 'Voltage', 'Brand', 'Is_kit', 'Is_gaming']] = raw_df['title'].apply(extract_ram_details)
    raw_df['Final_Price'] = raw_df['price'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
    print(raw_df)

    raw_df = raw_df.drop_duplicates(subset=['asin'])
    raw_df = raw_df.dropna(subset=['asin'])
    raw_df['Brand'] = raw_df['Brand'].fillna("unknown") # None / "unknown" (_all specific)
    print(raw_df)

    raw_df = raw_df[(raw_df['Speed_MHz'] >= 1000) & (raw_df['Speed_MHz'] < 10000)]
    raw_df = raw_df[(raw_df['Voltage'] < 2) & (raw_df['Voltage'] > 0)]
    #raw_df = raw_df[(raw_df['Capacity_GB'] > 16) & (raw_df['Capacity_GB'] <= 256)]   #(_PC Specific)
    #raw_df = raw_df[raw_df['Capacity_GB'] <= 32]   #(_PC2 Specific)
    raw_df = raw_df[(raw_df['Capacity_GB'] >= 32)]   #(_all Specific)
    raw_df = raw_df[['title', 'Capacity_GB', 'Generation', 'Speed_MHz', 'Latency', 'Voltage', 'Brand', 'Is_kit', 'Is_gaming', 'Final_Price']]
    clean_df = raw_df.dropna(subset=['title', 'Capacity_GB', 'Generation', 'Speed_MHz', 'Latency', 'Voltage', 'Brand', 'Is_kit', 'Is_gaming', 'Final_Price'])
    print(clean_df)

    return clean_df

dataset = clean_data()
print(dataset)

with open("../data/ram_data_cleaned.csv", "w", encoding='utf-8', newline='') as file:
    dataset.to_csv(file, index=False, encoding='utf-8')


check = []
check_unique = []
check.extend(dataset.Capacity_GB)
check_unique.extend(dataset.Capacity_GB.unique())
print(check_unique)
print(check)


"""
plt.scatter(dataset['Capacity_GB'], dataset['Final_Price'])
plt.xlabel('Kapacita (GB)')
plt.ylabel('Cena ($)')
plt.title('Vztah kapacity a ceny')
plt.show()
"""