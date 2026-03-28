import random
import time
import requests
import json

api_key = ""

#2E8CFE0825164AB081917AF668D10A1D
#3C3D7706BD4F4B4CABD11071A893011C

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

pages = [13, 14, 15, 16, 17, 18]

all_results = []

def search_term_for_key(key, terms, results, pages):
    """
    Scrapping method
    :param key: api_key recieved after creating account on rainforest api
    :param terms: terms which scrapper is searching for
    :param results: array for saving scraped products
    :param pages: pages through which is scraping
    :return: nothing - only of key is not provided
    """
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

        #průběžně ukládám pro ochranu
        with open('../data/ram_data_TEST3.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

search_term_for_key(api_key, search_terms, all_results, pages)

print(f"Data were downloaded! ({len(all_results)} products)")