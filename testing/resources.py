"""
Resource Tests
Test the Pokémon data resource functionality
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resource_encyclopedia.poke_data import PokemonDataResource

async def test_get_pokemon_data():
    """Test fetching individual Pokémon data"""
    print("=== Testing Pokémon Data Retrieval ===")
    
    pokemon_resource = PokemonDataResource()
    
    try:
        # Test popular Pokémon
        pokemon_names = ["pikachu", "charmander", "bulbasaur", "squirtle"]
        
        for name in pokemon_names:
            print(f"\nFetching data for {name.title()}...")
            data = await pokemon_resource.get_pokemon_data(name)
            
            print(f"ID: {data['id']}")
            print(f"Name: {data['name'].title()}")
            print(f"Types: {', '.join(data['types'])}")
            print(f"Base Stats: {data['base_stats']}")
            print(f"Abilities: {[ability['name'] for ability in data['abilities']]}")
            print(f"Number of moves: {len(data['moves'])}")
            if data['evolution_chain']:
                print(f"Evolution chain: {len(data['evolution_chain'])} stages")
            
    except Exception as e:
        print(f"Error: {e}")

async def test_pokemon_list():
    """Test fetching Pokémon list"""
    print("\n=== Testing Pokémon List ===")
    
    pokemon_resource = PokemonDataResource()
    
    try:
        data = await pokemon_resource.list_all_pokemon()
        
        print(f"Total Pokémon available: {data['count']}")
        print(f"First 10 Pokémon: {data['pokemon'][:10]}")
        
    except Exception as e:
        print(f"Error: {e}")

async def test_type_effectiveness():
    """Test type effectiveness data"""
    print("\n=== Testing Type Effectiveness ===")
    
    pokemon_resource = PokemonDataResource()
    
    try:
        effectiveness = await pokemon_resource.get_type_effectiveness("fire")
        
        print("Fire type effectiveness:")
        print(f"Super effective against: {effectiveness['double_damage_to']}")
        print(f"Not very effective against: {effectiveness['half_damage_to']}")
        print(f"No effect against: {effectiveness['no_damage_to']}")
        
    except Exception as e:
        print(f"Error: {e}")

async def test_invalid_pokemon():
    """Test handling of invalid Pokémon names"""
    print("\n=== Testing Invalid Pokémon ===")
    
    pokemon_resource = PokemonDataResource()
    
    try:
        data = await pokemon_resource.get_pokemon_data("invalidpokemon")
        print("This should not print")
        
    except Exception as e:
        print(f"Expected error: {e}")

async def test_caching():
    """Test caching mechanism"""
    print("\n=== Testing Caching ===")
    
    pokemon_resource = PokemonDataResource()
    
    try:
        print("First request for Pikachu (should fetch from API)...")
        import time
        start_time = time.time()
        data1 = await pokemon_resource.get_pokemon_data("pikachu")
        first_request_time = time.time() - start_time
        
        print("Second request for Pikachu (should use cache)...")
        start_time = time.time()
        data2 = await pokemon_resource.get_pokemon_data("pikachu")
        second_request_time = time.time() - start_time
        
        print(f"First request time: {first_request_time:.3f}s")
        print