import random
import time
import requests
import json

#Doplnit klíč
api_key = ""

search_terms = [
    "DDR4 RAM 16GB kit 3200MHz",
    "DDR5 RAM 32GB kit 6000MHz",
    "DDR4 RAM 8GB desktop",
    "DDR3 RAM 16GB kit",
    "SO-DIMM DDR4 16GB laptop",
    "SO-DIMM DDR5 32GB laptop",
    "SO-DIMM DDR3L 8GB",
    "Corsair Vengeance LPX",
    "G.SKILL Ripjaws V",
    "Kingston FURY Beast",
    "Crucial RAM DDR4",
    "Samsung RAM 8GB DDR4",
    "ECC RDIMM 32GB server",
    "Timetec Hynix IC RAM",
    "Patriot Viper Steel DDR4"
]

pages = [7, 8, 9, 10, 11, 12]

all_results = []

def search_term_for_key(key, terms, results, pages):
    if not key:
        print("Skipping: Key not provided.")
        return

    for search_term in terms:
        for page in pages:
            params = {
                'api_key': key,
                'type': 'search',
                'amazon_domain': 'amazon.com',
                'search_term': search_term,
                'page': str(page)
            }

            # kdyby to poslalo blbou stránku (prázdnou/žádnou,...)
            try:
                response = requests.get('https://api.rainforestapi.com/request', params)
                data = response.json()

                if "search_results" in data:
                    results.extend(data["search_results"])
                    print(f"Obtained {len(data['search_results'])} products")
                else:
                    print("No search results found")

            except Exception as e:
                print(f"Error occured: {e}")

            time.sleep(random.uniform(1, 4))

        final_data = {"data": all_results}

        with open('ram_data_TEST2.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

search_term_for_key(api_key, search_terms, all_results, pages)

"""
final_data = { "data": all_results }

with open('ram_data_TEST.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)
"""

print(f"Data were downloaded! ({len(all_results)} products)")