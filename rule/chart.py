"""
Type Effectiveness Chart
Handles Pokémon type effectiveness calculations
"""
from typing import Dict, List

class TypeChart:
    def __init__(self):
        self.effectiveness_chart = {
            'normal': {'rock': 0.5, 'ghost': 0.0, 'steel': 0.5},
            'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2.0, 'ice': 2.0,
                     'bug': 2.0, 'rock': 0.5, 'dragon': 0.5, 'steel': 2.0},
            'water': {'fire': 2.0, 'water': 0.5, 'grass': 0.5, 'ground': 2.0,
                      'rock': 2.0, 'dragon': 0.5},
            'electric': {'water': 2.0, 'electric': 0.5, 'grass': 0.5, 'ground': 0.0,
                         'flying': 2.0, 'dragon': 0.5},
            'grass': {'fire': 0.5, 'water': 2.0, 'grass': 0.5, 'poison': 0.5,
                      'ground': 2.0, 'flying': 0.5, 'bug': 0.5, 'rock': 2.0,
                      'dragon': 0.5, 'steel': 0.5},
            'ice': {'fire': 0.5, 'water': 0.5, 'grass': 2.0, 'ice': 0.5,
                    'ground': 2.0, 'flying': 2.0, 'dragon': 2.0, 'steel': 0.5},
            'fighting': {'normal': 2.0, 'ice': 2.0, 'poison': 0.5, 'flying': 0.5,
                         'psychic': 0.5, 'bug': 0.5, 'rock': 2.0, 'ghost': 0.0,
                         'dark': 2.0, 'steel': 2.0, 'fairy': 0.5},
            'poison': {'grass': 2.0, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5,
                       'ghost': 0.5, 'steel': 0.0, 'fairy': 2.0},
            'ground': {'fire': 2.0, 'electric': 2.0, 'grass': 0.5, 'poison': 2.0,
                       'flying': 0.0, 'bug': 0.5, 'rock': 2.0, 'steel': 2.0},
            'flying': {'electric': 0.5, 'grass': 2.0, 'ice': 0.5, 'fighting': 2.0,
                       'bug': 2.0, 'rock': 0.5, 'steel': 0.5},
            'psychic': {'fighting': 2.0, 'poison': 2.0, 'psychic': 0.5,
                        'dark': 0.0, 'steel': 0.5},
            'bug': {'fire': 0.5, 'grass': 2.0, 'fighting': 0.5, 'poison': 0.5,
                    'flying': 0.5, 'psychic': 2.0, 'ghost': 0.5, 'dark': 2.0,
                    'steel': 0.5, 'fairy': 0.5},
            'rock': {'fire': 2.0, 'ice': 2.0, 'fighting': 0.5, 'ground': 0.5,
                     'flying': 2.0, 'bug': 2.0, 'steel': 0.5},
            'ghost': {'normal': 0.0, 'psychic': 2.0, 'ghost': 2.0, 'dark': 0.5},
            'dragon': {'dragon': 2.0, 'steel': 0.5, 'fairy': 0.0},
            'dark': {'fighting': 0.5, 'psychic': 2.0, 'ghost': 2.0,
                     'dark': 0.5, 'fairy': 0.5},
            'steel': {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2.0,
                      'rock': 2.0, 'steel': 0.5, 'fairy': 2.0},
            'fairy': {'fire': 0.5, 'fighting': 2.0, 'poison': 0.5,
                      'dragon': 2.0, 'dark': 2.0, 'steel': 0.5}
        }
    
    def get_effectiveness(self, attacking_type: str, defending_type: str) -> float:
        """Return effectiveness multiplier for one type vs another"""
        return self.effectiveness_chart.get(attacking_type.lower(), {}).get(defending_type.lower(), 1.0)
    
    def get_all_effectiveness(self, attacking_type: str, defending_types: List[str]) -> float:
        """Effectiveness against multiple defending types"""
        multiplier = 1.0
        for t in defending_types:
            multiplier *= self.get_effectiveness(attacking_type, t)
        return multiplier
    
    def get_weaknesses(self, pokemon_types: List[str]) -> Dict[str, float]:
        """Get weaknesses for given Pokémon types"""
        all_types = [
            'normal', 'fire', 'water', 'electric', 'grass', 'ice',
            'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
            'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'
        ]
        return {atk: self.get_all_effectiveness(atk, pokemon_types)
                for atk in all_types
                if self.get_all_effectiveness(atk, pokemon_types) != 1.0}
    
    def get_resistances(self, pokemon_types: List[str]) -> Dict[str, float]:
        """Get resistances (types doing reduced damage)"""
        return {t: eff for t, eff in self.get_weaknesses(pokemon_types).items() if eff < 1.0}
    
    def get_super_effective_against(self, attacking_type: str) -> List[str]:
        """Return types this attack is strong against"""
        return [d for d, eff in self.effectiveness_chart.get(attacking_type.lower(), {}).items() if eff > 1.0]
