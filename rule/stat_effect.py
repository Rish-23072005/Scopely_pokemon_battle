"""
Status Effect Management
Handles Pokémon status conditions and their effects
"""
import random
from typing import Dict, Any, Optional

class StatusEffectManager:
    def __init__(self):
        self.status_move_effects = {
            'thunderbolt': {'status': 'paralysis', 'chance': 0.1},
            'thunder': {'status': 'paralysis', 'chance': 0.3},
            'flame-thrower': {'status': 'burn', 'chance': 0.1},
            'fire-blast': {'status': 'burn', 'chance': 0.1},
            'ice-beam': {'status': 'freeze', 'chance': 0.1},
            'blizzard': {'status': 'freeze', 'chance': 0.1},
            'poison-sting': {'status': 'poison', 'chance': 0.3},
            'toxic': {'status': 'badly_poison', 'chance': 0.9},
            'sleep-powder': {'status': 'sleep', 'chance': 0.75},
            'hypnosis': {'status': 'sleep', 'chance': 0.6},
        }
    
    def apply_status_effects(self, target: Dict[str, Any], move_name: str) -> Optional[str]:
        if target.get('status') and target['status'] != 'none':
            return None
        
        move_name = move_name.lower().replace(' ', '-')
        
        if move_name in self.status_move_effects:
            effect_data = self.status_move_effects[move_name]
            
            if random.random() < effect_data['chance']:
                status = effect_data['status']
                target['status'] = status
                target['status_turns'] = self._get_status_duration(status)
                
                return self._get_status_message(target['name'], status)
        
        return None
    
    def can_move(self, pokemon: Dict[str, Any]) -> bool:
        status = pokemon.get('status')
        
        if status == 'paralysis':
            if random.random() < 0.25:
                return False
        elif status == 'freeze':
            if random.random() < 0.2:
                pokemon['status'] = None
                pokemon['status_turns'] = 0
                return True
            return False
        elif status == 'sleep':
            if pokemon.get('status_turns', 0) > 0:
                pokemon['status_turns'] -= 1
                if pokemon['status_turns'] <= 0:
                    pokemon['status'] = None
                return False
        
        return True
    
    def process_end_turn_status(self, pokemon: Dict[str, Any]) -> int:
        status = pokemon.get('status')
        damage = 0
        
        if status == 'burn':
            damage = max(1, pokemon['max_hp'] // 16)
            pokemon['current_hp'] = max(0, pokemon['current_hp'] - damage)
        
        elif status == 'poison':
            damage = max(1, pokemon['max_hp'] // 8)
            pokemon['current_hp'] = max(0, pokemon['current_hp'] - damage)
        
        elif status == 'badly_poison':
            turns_poisoned = pokemon.get('poison_counter', 1)
            damage = max(1, (pokemon['max_hp'] * turns_poisoned) // 16)
            pokemon['current_hp'] = max(0, pokemon['current_hp'] - damage)
            pokemon['poison_counter'] = turns_poisoned + 1
        
        if pokemon.get('status_turns', 0) > 0:
            pokemon['status_turns'] -= 1
            if pokemon['status_turns'] <= 0:
                pokemon['status'] = None
        
        return damage
    
    def _get_status_duration(self, status: str) -> int:
        durations = {
            'sleep': random.randint(1, 3),
            'freeze': 999,
            'paralysis': 999,
            'burn': 999,
            'poison': 999,
            'badly_poison': 999,
        }
        return durations.get(status, 0)
    
    def _get_status_message(self, pokemon_name: str, status: str) -> str:
        messages = {
            'paralysis': f"{pokemon_name.title()} was paralyzed!",
            'burn': f"{pokemon_name.title()} was burned!",
            'freeze': f"{pokemon_name.title()} was frozen solid!",
            'poison': f"{pokemon_name.title()} was poisoned!",
            'badly_poison': f"{pokemon_name.title()} was badly poisoned!",
            'sleep': f"{pokemon_name.title()} fell asleep!",
        }
        return messages.get(status, f"{pokemon_name.title()} was affected by {status}!")
    
    def cure_status(self, pokemon: Dict[str, Any]) -> str:
        old_status = pokemon.get('status')
        pokemon['status'] = None
        pokemon['status_turns'] = 0
        pokemon['poison_counter'] = 0
        
        if old_status and old_status != 'none':
            return f"{pokemon['name'].title()}'s {old_status} was cured!"
        return ""
    
    def get_status_info(self, pokemon: Dict[str, Any]) -> Dict[str, Any]:
        status = pokemon.get('status')
        
        if not status or status == 'none':
            return {'status': 'none', 'description': 'No status effects'}
        
        info = {
            'status': status,
            'turns_remaining': pokemon.get('status_turns', 0),
            'description': self._get_status_description(status)
        }
        
        if status == 'badly_poison':
            info['poison_counter'] = pokemon.get('poison_counter', 1)
        
        return info
    
    def _get_status_description(self, status: str) -> str:
        descriptions = {
            'paralysis': 'Cannot move 25% of the time, Speed reduced by 75%',
            'burn': 'Takes damage each turn, physical attack reduced by 50%',
            'freeze': 'Cannot move, 20% chance to thaw each turn',
            'poison': 'Takes 1/8 max HP damage each turn',
            'badly_poison': 'Takes increasing damage each turn',
            'sleep': 'Cannot move for 1-3 turns',
        }
        return descriptions.get(status, 'Unknown status effect')
    
    def modify_speed(self, pokemon: Dict[str, Any]) -> int:
        base_speed = pokemon['speed']
        
        if pokemon.get('status') == 'paralysis':
            return base_speed // 4
        return base_speed
    
    def modify_attack(self, pokemon: Dict[str, Any], move_category: str) -> int:
        if move_category.lower() == 'physical':
            base_attack = pokemon['attack']
            if pokemon.get('status') == 'burn':
                return base_attack // 2
            return base_attack
        else:
            return pokemon['special_attack']
