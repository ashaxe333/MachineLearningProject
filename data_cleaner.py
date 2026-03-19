import json
import re
import pandas as pd

gen_freq_dict = {
    "PC3-8500": 1066.0,
    "PC3-10600": 1333.0,
    "PC3-12800": 1600.0,
    "PC3-14900": 1866.0,
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

raw_df = pd.DataFrame(raw_data["data"])

def extract_ram_details(title):

    size = re.search(r'(\d+(?:\.\d+)?)\s*(MB|GB)', title, re.IGNORECASE)  #(\d+(?:\.\d+)?)\s*(GB|MB) - pro desetinná čísla

    gen = re.search(r'DDR(\d)L*', title, re.IGNORECASE)

    freq_match = re.search(r'(\d+(?:\.\d+)?)\s*(MHz|MH|GHz|MT/s)', title, re.IGNORECASE)
    freq = None

    if freq_match:
        freq_value = float(freq_match.group(1))
        freq_unit = str(freq_match.group(2))
        freq = freq_value * 1000 if freq_unit == 'GHz' else freq_value

    if freq_match is None:
        freq_match = re.search(r'(DDR(\d)L*)\s*-*(\d+(?:\.\d+)?)', title, re.IGNORECASE)
        if freq_match:
            freq = float(freq_match.group(3))

    if freq_match is None:
        freq_match = re.search(r'(PC\d)\s*-*(\d+(?:\.\d+)?)', title, re.IGNORECASE)
        if freq_match:
            freq_type = str(freq_match.group(1)).upper()
            freq_value = str(freq_match.group(2))
            if len(freq_value) == 4 and int(freq_value[0]) < 6:
                freq = freq_value
            else:
                freq_key = f"{freq_type}-{freq_value}"
                freq = gen_freq_dict.get(freq_key)

    brand = re.search(r'(Corsair|G.SKILL|Crucial|TEAMGROUP|Kingston|XPG|Samsung|PNY|Timetec|ADATA|SK Hynix|A-Tech|OWC|Micron|Ballistix|HP|Dell|Patriot Memory|Patriot|Lenovo|QNAP|Adamanta)', title, re.IGNORECASE)

    latency = re.search(r'(CL|C)(\d+)', title, re.IGNORECASE)

    """
    if latency is None:
        print(f"latency none in: {title}")
    if size is None:
        print(f"size none in: {title}")
    if gen is None:
        print(f"gen none in: {title}")
    if freq is None:
        print(f"freq none in: {title}")
    if freq:
        #print(f"freq: {freq}")
        if freq < 1066:
            print(f"freq is {freq} in: {title}")"""


    return pd.Series([
        float(size.group(1)) if size else None,
        int(gen.group(1)) if gen else None,
        freq,
        str(brand.group(1)) if brand else None,
        str(latency.group(1)) if latency else None
    ])

#print(raw_df.head())
raw_df[['Capacity_GB', 'Generation', 'Speed_MHz', 'Brand', 'Latency']] = raw_df['title'].apply(extract_ram_details)
raw_df['Final_Price'] = raw_df['price'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
raw_df = raw_df.drop_duplicates(subset=['asin'])
raw_df['Brand'] = raw_df['Brand'].fillna('Unknown')
print(raw_df)
df_clean = raw_df.dropna(subset=['Capacity_GB', 'Generation', 'Speed_MHz', 'Brand', 'Latency', 'Final_Price'])
print(df_clean)
#print(df_clean.head())



"""
new_df = pd.DataFrame(['Capacity_GB', 'Generation', 'Speed_MHz', 'Brand'])
new_df[['Capacity_GB', 'Generation', 'Speed_MHz', 'Brand']] = raw_df['title'].apply(extract_ram_details)
new_df['Final_Price'] = raw_df['price'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
new_df = raw_df.drop_duplicates(subset=['asin'])
new_df['Brand'] = raw_df['Brand'].fillna('Unknown')
print(new_df)
df_clean = new_df.dropna(subset=['Capacity_GB', 'Generation', 'Speed_MHz', 'Final_Price'])
print(df_clean)
"""