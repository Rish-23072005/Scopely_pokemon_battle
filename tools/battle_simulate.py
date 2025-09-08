import random
from resource_encyclopedia.poke_data import get_pokemon_data
from rule.chart import get_type_multiplier
from rule.damage_calcu import calculate_damage
from rule.stat_effect import apply_status, random_status

def simulate_battle(pokemon1: str, pokemon2: str) -> dict:
    """
    Simulates a Pokémon battle, robust to bad data and demonstrates detailed logs.
    """
    p1 = get_pokemon_data(pokemon1)
    p2 = get_pokemon_data(pokemon2)
    log = []

    # Handle the edge case of an invalid Pokémon name.
    if "error" in p1:
        return {"error": f"Invalid Pokémon name provided: {pokemon1}"}
    if "error" in p2:
        return {"error": f"Invalid Pokémon name provided: {pokemon2}"}

    # Initialize stats and moves with fallbacks for missing data.
    p1_hp = p1["stats"].get("hp", 50)
    p2_hp = p2["stats"].get("hp", 50)
    p1_speed = p1["stats"].get("speed", 50)
    p2_speed = p2["stats"].get("speed", 50)
    p1_moves = p1["moves"] if p1["moves"] else ["tackle"]
    p2_moves = p2["moves"] if p2["moves"] else ["tackle"]

    # Status effects for each Pokémon.
    p1_status = None
    p2_status = None

    turn = 1
    # Prevent infinite loops in the edge case of two defensive Pokémon.
    while p1_hp > 0 and p2_hp > 0 and turn <= 100:
        log.append(f"--- Turn {turn} ---")

        # Determine turn order based on speed and handle ties.
        first, first_hp, first_moves, first_status, first_name = (
            (p1, p1_hp, p1_moves, p1_status, pokemon1)
            if p1_speed > p2_speed or (p1_speed == p2_speed and turn % 2 == 1)
            else (p2, p2_hp, p2_moves, p2_status, pokemon2)
        )
        second, second_hp, second_moves, second_status, second_name = (
            (p2, p2_hp, p2_moves, p2_status, pokemon2)
            if first is p1
            else (p1, p1_hp, p1_moves, p1_status, pokemon1)
        )

        # Apply status effects at the beginning of the turn
        first_hp, missed_turn = apply_status(first_hp, first_status)
        if missed_turn:
            log.append(f"{first_name} was paralyzed and missed its attack!")
        else:
            if first_hp > 0:
                # Pick a random move and calculate damage.
                move_power = 40
                type_mult = get_type_multiplier(random.choice(first["types"]), second["types"])
                damage = calculate_damage(first, second, move_power, type_mult)
                second_hp -= damage
                log.append(f"{first_name} used a move, dealing {damage} damage. {second_name} HP is now {max(second_hp, 0)}.")

        # Check for fainting after the first attack.
        if second_hp <= 0:
            log.append(f"{second_name} fainted!")
            return {"winner": first_name, "battle_log": log}

        # Apply status effects to the second pokemon at the start of its turn
        second_hp, missed_turn2 = apply_status(second_hp, second_status)

        if not missed_turn2:
            if second_hp > 0: # Check if the first Pokémon didn't faint
                type_mult2 = get_type_multiplier(random.choice(second["types"]), first["types"])
                damage2 = calculate_damage(second, first, move_power, type_mult2) # pyright: ignore[reportPossiblyUnboundVariable]
                first_hp -= damage2
                log.append(f"{second_name} used a move, dealing {damage2} damage. {first_name} HP is now {max(first_hp, 0)}.")
            else:
                log.append(f"{second_name} was paralyzed and missed its attack!")

        # Check if a new status is applied to the defender.
        if first_hp > 0 and not first_status:
            status_applied2 = random_status()
            if status_applied2:
                first_status = status_applied2
                log.append(f"{first_name} is now affected by {status_applied2}.")

        if first_hp <= 0:
            log.append(f"{first_name} fainted!")
            return {"winner": second_name, "battle_log": log}

        # Update the main HP variables.
        if first is p1:
            p1_hp, p1_status = first_hp, first_status
            p2_hp, p2_status = second_hp, second_status
        else:
            p2_hp, p2_status = first_hp, first_status
            p1_hp, p1_status = second_hp, second_status

        turn += 1

    # In case of a timeout or infinite loop.
    return {"winner": "Draw", "battle_log": log + ["Battle ended after 100 turns, no winner."]}
