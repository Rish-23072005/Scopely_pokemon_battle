import random

def apply_status(current_hp: int, status: str) -> tuple[int, bool]:
    """
    Implements Burn, Poison, Paralysis. Handles status persistence and randomization.
    Returns the new HP and whether the turn was missed.
    """
    missed_turn = False
    
    if status == "burn":
        current_hp -= max(int(current_hp * 0.0625), 1)
    elif status == "poison":
        current_hp -= max(int(current_hp * 0.125), 1)
    elif status == "paralysis":
        if random.random() < 0.25:
            missed_turn = True
            
    current_hp = max(current_hp, 0)
    return current_hp, missed_turn

def random_status() -> str | None:
    """
    Randomly selects a status effect or None to apply to a Pokémon.
    """
    return random.choice(["burn", "poison", "paralysis", None, None])
