import time
import requests
import json

#api_key = "F0109579D9FA4CAD80FBACF23DD58A66"
api_keys = ["F0109579D9FA4CAD80FBACF23DD58A66", "A37574553F5645F2AA9680EE504E6993", "33B6590F1D48481BAEA8B60842C07BD3"]

search_terms1 = ["DDR4 RAM 16GB", "DDR4 RAM 32GB", "DDR5 RAM 16GB"]
search_terms2 = ["DDR5 RAM 32GB", "Laptop RAM 8GB", "Laptop RAM 16GB", "DDR5 96GB Kit"]
search_terms3 = ["DDR3 RAM 8GB", "G.Skill Trident Z", "Corsair Vengeance DDR5", "Crucial RAM DDR4"]

pages = [1, 2, 3, 4, 5]

all_results = []

def search_term_for_key(key, terms, results):
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

            try:
                response = requests.get('https://api.rainforestapi.com/request', params)
                data = response.json()

                if "search_results" in data:
                    results.extend(data["search_results"])
                    print(f"Obtained {len(data["search_results"])} products")
                else:
                    print("No search results found")

            except Exception as e:
                print(f"Error occured: {e}")

            time.sleep(1)

"""
search_term_for_key(api_keys[0], search_terms1, all_results))
search_term_for_key(api_keys[1], search_terms2, all_results)
search_term_for_key(api_keys[2], search_terms3, all_results)
"""

final_data = { "data": all_results }

with open('ram_data_page1.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"Data were downloaded! ({len(all_results)} products)")