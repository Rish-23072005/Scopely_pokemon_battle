"""
Damage Calculation Engine
Handles Pokémon battle damage calculations with proper formulas
"""
import random
from typing import Dict, Any

class DamageCalculator:
    def __init__(self):
        pass
    
    def calculate_damage(self, attacker: Dict[str, Any], defender: Dict[str, Any], 
                        move_power: int, move_type: str, move_category: str, 
                        type_effectiveness: float) -> int:
        """
        Calculate damage using the Pokémon damage formula
        
        Formula: ((((2*Level/5+2)*Power*A/D)/50)+2)*Modifiers
        """
        level = attacker['level']
        power = move_power
        
        if move_category.lower() == 'special':
            attack_stat = attacker['special_attack']
            defense_stat = defender['special_defense']
        else:  
            attack_stat = attacker['attack']
            defense_stat = defender['defense']
        
        damage = (((2 * level / 5 + 2) * power * attack_stat / defense_stat) / 50 + 2)
        
        modifiers = 1.0
        
        # Same-Type Attack Bonus (STAB)
        if move_type.lower() in [t.lower() for t in attacker['types']]:
            modifiers *= 1.5
        
        # Type effectiveness
        modifiers *= type_effectiveness
        
        # Random factor (85-100%)
        random_factor = random.uniform(0.85, 1.0)
        modifiers *= random_factor
        
        # Critical hit chance (6.25% base chance)
        if random.random() < 0.0625:
            modifiers *= 2.0
        
        final_damage = int(damage * modifiers)
        
        if final_damage < 1 and type_effectiveness > 0:
            final_damage = 1
        
        return final_damage
    
    def calculate_stat_at_level(self, base_stat: int, level: int, iv: int = 31, ev: int = 0) -> int:
        return int(((2 * base_stat + iv + ev // 4) * level / 100) + 5)
    
    def calculate_hp_at_level(self, base_hp: int, level: int, iv: int = 31, ev: int = 0) -> int:
        return int(((2 * base_hp + iv + ev // 4) * level / 100) + level + 10)
    
    def get_critical_hit_multiplier(self, critical_hit_stage: int = 0) -> float:
        critical_hit_rates = {
            0: 0.0625,  # 1/16
            1: 0.125,   # 1/8
            2: 0.25,    # 1/4
            3: 0.333,   # 1/3
            4: 0.5      # 1/2
        }
        
        stage = min(4, max(0, critical_hit_stage))
        return critical_hit_rates.get(stage, 0.0625)
    
    def apply_burn_reduction(self, damage: int, attacker_status: str, move_category: str) -> int:
        if attacker_status == 'burn' and move_category.lower() == 'physical':
            return damage // 2
        return damage
    
    def calculate_recoil_damage(self, damage_dealt: int, recoil_percentage: float) -> int:
        return max(1, int(damage_dealt * recoil_percentage))
    
    def calculate_recovery_amount(self, max_hp: int, recovery_percentage: float) -> int:
        return max(1, int(max_hp * recovery_percentage))
    
    def get_damage_roll_description(self, damage: int, max_possible: int) -> str:
        if max_possible == 0:
            return "No damage"
        
        percentage = (damage / max_possible) * 100
        
        if percentage >= 95:
            return "Maximum damage roll"
        elif percentage >= 90:
            return "High damage roll"
        elif percentage >= 75:
            return "Good damage roll"
        elif percentage >= 50:
            return "Average damage roll"
        elif percentage >= 25:
            return "Low damage roll"
        else:
            return "Minimum damage roll"
