from tools.battle_simulate import simulate_battle

def test_battle_normal():
    """Test a standard battle between two valid Pokémon."""
    result = simulate_battle("charmander", "bulbasaur")
    assert "winner" in result
    assert isinstance(result["battle_log"], list)
    assert result["winner"] in ["charmander", "bulbasaur", "Draw"]

def test_battle_invalid_pokemon():
    """Test the case where one Pokémon name is invalid."""
    result = simulate_battle("foo", "pikachu")
    assert "error" in result
    assert "notapokemon" not in result["error"]
    assert "pikachu" not in result["error"]

def test_battle_draw():
    """Test a scenario that should result in a draw."""
    # We can use two highly defensive Pokémon to force a draw.
    result = simulate_battle("blissey", "chansey")
    assert result["winner"] == "Draw"
