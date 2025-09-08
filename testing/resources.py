from resource_encyclopedia.poke_data import get_pokemon_data

def test_valid_pokemon():
    """Test fetching data for a valid Pokémon."""
    pikachu = get_pokemon_data("pikachu")
    assert "error" not in pikachu
    assert pikachu["name"] == "pikachu"
    assert "electric" in pikachu["types"]

def test_invalid_pokemon():
    """Test fetching data for an invalid Pokémon name."""
    missing = get_pokemon_data("notapokemon")
    assert "error" in missing
    assert "not found" in missing["error"]

def test_pokemon_with_missing_data():
    """Test a Pokémon that might have missing data (e.g., placeholder)."""
    # Using a known valid pokemon, but assuming the API might return incomplete data.
    # Our function should provide default values.
    data = get_pokemon_data("snorlax")
    assert "hp" in data["stats"]
    assert "tackle" in data["moves"] or len(data["moves"]) > 0
