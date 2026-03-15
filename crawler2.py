import time
import requests
import json

api_key = "F0109579D9FA4CAD80FBACF23DD58A66"

search_terms = ["DDR4 RAM 16GB", "DDR4 RAM 32GB"]

""", "DDR5 RAM 16GB", "DDR5 RAM 32GB",
    "Laptop RAM 8GB", "Laptop RAM 16GB", "DDR3 RAM 8GB", "G.Skill Trident Z",
    "Corsair Vengeance DDR5", "Crucial RAM DDR4"""

pages = [1, 2]

all_results = []

for search_term in search_terms:
    for page in pages:
        params = {
          'api_key': api_key,
          'type': 'search',
          'amazon_domain': 'amazon.com',
          'search_term': search_term,
          'page': str(page)
        }

        try:
            # Odeslání požadavku
            response = requests.get('https://api.rainforestapi.com/request', params)
            # Převod na JSON
            data = response.json()

            if "search_results" in data:
                all_results.extend(data["search_results"])
                print(f"Obtained {len(data["search_results"])} products")
            else:
                print("No search results found")

        except Exception as e:
            print(f"Error occured: {e}")

        time.sleep(1)

final_data = { "data": all_results }

# Uložení do souboru
with open('ram_data_page1.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"Data were downloaded! ({len(all_results)} products)")