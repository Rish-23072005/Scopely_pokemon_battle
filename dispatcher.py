from tools.battle_simulate import simulate_battle
from resource_encyclopedia.poke_data import get_pokemon_data

def handle_request(request: dict) -> dict:
    """
    Handles incoming requests robustly (edge: unknown action, missing fields).
    """
    if not isinstance(request, dict):
        return {"error": "Request is not a valid JSON object."}
    
    action = request.get("action")
    
    if action == "battle":
        pk1 = request.get("pokemon1")
        pk2 = request.get("pokemon2")
        if not pk1 or not pk2:
            return {"error": "Missing Pokémon name(s) for battle."}
        return simulate_battle(pk1, pk2)
    elif action == "info":
        pk = request.get("pokemon")
        if not pk:
            return {"error": "Missing Pokémon name for info."}
        return get_pokemon_data(pk)
    else:
        return {"error": "Unknown action. Supported: battle, info"}
