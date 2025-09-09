"""
Battle Simulation Tool
MCP tool for simulating Pokémon battles
"""
import random
from typing import Dict, Any, Tuple
import logging
from resource_encyclopedia.poke_data import PokemonDataResource
from rule.chart import TypeChart
from rule.damage_calcu import DamageCalculator
from rule.stat_effect import StatusEffectManager

logger = logging.getLogger(__name__)

class BattleSimulationTool:
    """Pokémon battle simulation engine"""

    def __init__(self):
        self.pokemon_data = PokemonDataResource()
        self.type_chart = TypeChart()
        self.damage_calculator = DamageCalculator()
        self.status_manager = StatusEffectManager()
    
    async def simulate_battle(self, pokemon1_name: str, pokemon2_name: str, 
                              level1: int = 50, level2: int = 50) -> Dict[str, Any]:
        """Run a complete battle simulation between two Pokémon"""
        try:
            pokemon1_data = await self.pokemon_data.get_pokemon_data(pokemon1_name)
            pokemon2_data = await self.pokemon_data.get_pokemon_data(pokemon2_name)
            pokemon1 = self._create_battle_pokemon(pokemon1_data, level1)
            pokemon2 = self._create_battle_pokemon(pokemon2_data, level2)
            
            battle_log = [
                "=== BATTLE START ===",
                f"{pokemon1['name'].title()} (Lv.{level1}) VS {pokemon2['name'].title()} (Lv.{level2})",
                f"{pokemon1['name'].title()}: HP {pokemon1['current_hp']}/{pokemon1['max_hp']}",
                f"{pokemon2['name'].title()}: HP {pokemon2['current_hp']}/{pokemon2['max_hp']}",
                ""
            ]
            
            turn = 1
            winner = None
            
            while pokemon1['current_hp'] > 0 and pokemon2['current_hp'] > 0 and turn <= 100:
                battle_log.append(f"--- Turn {turn} ---")
                first, second = self._determine_turn_order(pokemon1, pokemon2)
                
                if first['current_hp'] > 0:
                    damage, move_used, effectiveness = await self._execute_turn(first, second)
                    battle_log.append(f"{first['name'].title()} used {move_used}!")
                    if effectiveness > 1.0:
                        battle_log.append("It's super effective!")
                    elif 0 < effectiveness < 1.0:
                        battle_log.append("It's not very effective...")
                    elif effectiveness == 0:
                        battle_log.append("It had no effect...")
                    if damage > 0:
                        battle_log.append(f"{second['name'].title()} took {damage} damage!")
                    status_message = self.status_manager.apply_status_effects(second, move_used)
                    if status_message:
                        battle_log.append(status_message)
                
                if second['current_hp'] <= 0:
                    battle_log.append(f"{second['name'].title()} fainted!")
                    winner = first['name']
                    break
                
                if second['current_hp'] > 0:
                    damage, move_used, effectiveness = await self._execute_turn(second, first)
                    battle_log.append(f"{second['name'].title()} used {move_used}!")
                    if effectiveness > 1.0:
                        battle_log.append("It's super effective!")
                    elif 0 < effectiveness < 1.0:
                        battle_log.append("It's not very effective...")
                    elif effectiveness == 0:
                        battle_log.append("It had no effect...")
                    if damage > 0:
                        battle_log.append(f"{first['name'].title()} took {damage} damage!")
                    status_message = self.status_manager.apply_status_effects(first, move_used)
                    if status_message:
                        battle_log.append(status_message)
                
                if first['current_hp'] <= 0:
                    battle_log.append(f"{first['name'].title()} fainted!")
                    winner = second['name']
                    break
                
                for pokemon in [first, second]:
                    status_damage = self.status_manager.process_end_turn_status(pokemon)
                    if status_damage > 0:
                        battle_log.append(f"{pokemon['name'].title()} took {status_damage} damage from {pokemon['status']}!")
                        if pokemon['current_hp'] <= 0:
                            battle_log.append(f"{pokemon['name'].title()} fainted from {pokemon['status']}!")
                            winner = second['name'] if pokemon == first else first['name']
                            break
                if winner:
                    break
                
                battle_log.append(f"{pokemon1['name'].title()}: {pokemon1['current_hp']}/{pokemon1['max_hp']} HP")
                battle_log.append(f"{pokemon2['name'].title()}: {pokemon2['current_hp']}/{pokemon2['max_hp']} HP")
                battle_log.append("")
                turn += 1
            
            if not winner and turn > 100:
                winner = "Draw (Battle limit reached)"
                battle_log.append("Battle ended in a draw due to turn limit!")
            else:
                battle_log.append("=== BATTLE END ===")
                battle_log.append(f"Winner: {winner.title()}!")
            
            return {
                "winner": winner,
                "total_turns": turn - 1,
                "battle_log": "\n".join(battle_log),
                "summary": f"{winner.title()} wins the battle in {turn-1} turns!",
                "final_stats": {
                    pokemon1['name']: {
                        "hp_remaining": pokemon1['current_hp'],
                        "max_hp": pokemon1['max_hp'],
                        "status": pokemon1.get('status', 'none')
                    },
                    pokemon2['name']: {
                        "hp_remaining": pokemon2['current_hp'],
                        "max_hp": pokemon2['max_hp'],
                        "status": pokemon2.get('status', 'none')
                    }
                }
            }
        except Exception as e:
            logger.error(f"Error in battle simulation: {e}")
            raise ValueError(f"Battle simulation failed: {e}")
    
    def _create_battle_pokemon(self, pokemon_data: Dict[str, Any], level: int) -> Dict[str, Any]:
        """Prepare a Pokémon with calculated stats for battle"""
        base_stats = pokemon_data['base_stats']
        hp = int(((2 * base_stats['hp'] * level) / 100) + level + 10)
        attack = int(((2 * base_stats['attack'] * level) / 100) + 5)
        defense = int(((2 * base_stats['defense'] * level) / 100) + 5)
        sp_attack = int(((2 * base_stats['special_attack'] * level) / 100) + 5)
        sp_defense = int(((2 * base_stats['special_defense'] * level) / 100) + 5)
        speed = int(((2 * base_stats['speed'] * level) / 100) + 5)
        return {
            'name': pokemon_data['name'],
            'level': level,
            'types': pokemon_data['types'],
            'max_hp': hp,
            'current_hp': hp,
            'attack': attack,
            'defense': defense,
            'special_attack': sp_attack,
            'special_defense': sp_defense,
            'speed': speed,
            'moves': pokemon_data['moves'][:4],
            'status': None,
            'status_turns': 0
        }
    
    def _determine_turn_order(self, pokemon1: Dict, pokemon2: Dict) -> Tuple[Dict, Dict]:
        """Decide move order based on speed"""
        if pokemon1['speed'] > pokemon2['speed']:
            return pokemon1, pokemon2
        elif pokemon2['speed'] > pokemon1['speed']:
            return pokemon2, pokemon1
        return (pokemon1, pokemon2) if random.random() < 0.5 else (pokemon2, pokemon1)
    
    async def _execute_turn(self, attacker: Dict, defender: Dict) -> Tuple[int, str, float]:
        """Perform a move and return damage dealt"""
        if not self.status_manager.can_move(attacker):
            return 0, "struggled", 1.0
        move = random.choice(attacker['moves']) if attacker['moves'] else {
            "name": "tackle", "details": {"type": "normal", "category": "physical", "power": 40}
        }
        move_name = move['name']
        details = move.get('details', {})
        move_type = details.get('type', 'normal')
        move_category = details.get('category', 'physical')
        move_power = details.get('power', 40) or 40
        effectiveness = 1.0
        for defender_type in defender['types']:
            effectiveness *= self.type_chart.get_effectiveness(move_type, defender_type)
        damage = self.damage_calculator.calculate_damage(
            attacker, defender, move_power, move_type, move_category, effectiveness
        )
        defender['current_hp'] = max(0, defender['current_hp'] - damage)
        return damage, move_name, effectiveness
