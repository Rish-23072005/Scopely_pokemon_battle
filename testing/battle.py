"""
Battle Simulation Tests
Test the battle simulation functionality
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.battle_simulate import BattleSimulationTool

async def test_basic_battle():
    """Test basic battle simulation"""
    print("=== Testing Basic Battle ===")
    
    battle_tool = BattleSimulationTool()
    
    try:
        result = await battle_tool.simulate_battle("pikachu", "charmander")
        
        print(f"Winner: {result['winner']}")
        print(f"Turns: {result['total_turns']}")
        print("\nBattle Log:")
        print(result['battle_log'])
        print("\nFinal Stats:")
        print(result['final_stats'])
        
    except Exception as e:
        print(f"Error: {e}")

async def test_level_difference():
    """Test battle with level differences"""
    print("\n=== Testing Level Difference Battle ===")
    
    battle_tool = BattleSimulationTool()
    
    try:
        result = await battle_tool.simulate_battle("pikachu", "charmander", 30, 60)
        
        print(f"Winner: {result['winner']}")
        print(f"Turns: {result['total_turns']}")
        print("\nSummary:")
        print(result['summary'])
        
    except Exception as e:
        print(f"Error: {e}")

async def test_type_advantage():
    """Test battle with clear type advantages"""
    print("\n=== Testing Type Advantage Battle ===")
    
    battle_tool = BattleSimulationTool()
    
    try:
        # Water vs Fire - clear advantage
        result = await battle_tool.simulate_battle("squirtle", "charmander")
        
        print("Squirtle (Water) vs Charmander (Fire)")
        print(f"Winner: {result['winner']}")
        print(f"Turns: {result['total_turns']}")
        
    except Exception as e:
        print(f"Error: {e}")

async def test_invalid_pokemon():
    """Test battle with invalid Pokémon names"""
    print("\n=== Testing Invalid Pokémon ===")
    
    battle_tool = BattleSimulationTool()
    
    try:
        result = await battle_tool.simulate_battle("invalidmon", "charmander")
        print("This should not print")
        
    except Exception as e:
        print(f"Expected error: {e}")

async def run_all_tests():
    """Run all battle tests"""
    print("Running Battle Simulation Tests...")
    
    await test_basic_battle()
    await test_level_difference()
    await test_type_advantage()
    await test_invalid_pokemon()
    
    print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    asyncio.run(run_all_tests())