import requests

def get_pokemon_data(name: str) -> dict:
    """
    Fetches comprehensive Pokémon data from PokeAPI, with fallback for missing info.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return {"error": "Pokémon not found"}
        
        data = resp.json()
        
        stats = {s["stat"]["name"]: s["base_stat"] for s in data.get("stats", [])}
        types = [t["type"]["name"] for t in data.get("types", [])]
        abilities = [a["ability"]["name"] for a in data.get("abilities", [])]
        moves = [m["move"]["name"] for m in data.get("moves", [])]
        
        # Handle edge cases with default values for missing data
        return {
            "name": data.get("name", name),
            "id": data.get("id", -1),
            "types": types if types else ["normal"],
            "stats": stats if stats else {"hp": 50, "attack": 50, "defense": 50, "speed": 50},
            "abilities": abilities,
            "moves": moves if moves else ["tackle"],
        }
    except requests.exceptions.RequestException:
        return {"error": "Network error while fetching Pokémon data."}
