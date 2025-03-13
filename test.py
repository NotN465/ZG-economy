import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    response_code = response.status_code
    if response_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failde to retrieve data {response_code}")
pokemon = "metapod"
pokemon_info = get_pokemon_info(pokemon)
if pokemon_info:
    print(f"{pokemon_info['name']}\n{pokemon_info['id']}\n{pokemon_info['height']},{pokemon_info['weight']}")