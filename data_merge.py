import json

with open("ram_data_TEST.json", "r", encoding='utf-8') as f:
    ram_data_TEST = json.load(f)

with open("ram_data_TEST2.json", "r", encoding='utf-8') as f:
    ram_data_TEST2 = json.load(f)

print(len(ram_data_TEST["data"]))

all_rows = []

all_rows.extend(ram_data_TEST["data"])
all_rows.extend(ram_data_TEST2["data"])

final_data = {"data": all_rows}

print(len(final_data["data"]))

with open("ram_data.json", "w", encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)