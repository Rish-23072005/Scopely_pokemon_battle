def calculate_damage(attacker: dict, defender: dict, move_power: int, type_mult: float) -> int:
    """
    Computes damage, handles missing stats/move power edge cases.
    """
    # Use default values if stats are missing to avoid errors.
    atk = attacker["stats"].get("attack", 50)
    defn = defender["stats"].get("defense", 50)
    power = move_power if isinstance(move_power, int) else 40
    
    # Ensure defense is never zero to prevent a ZeroDivisionError.
    damage = ((2 * 50 / 5 + 2) * power * atk / max(defn, 1)) / 50 + 2
    
    # Ensure a minimum damage of 1.
    return max(int(damage * type_mult), 1)
