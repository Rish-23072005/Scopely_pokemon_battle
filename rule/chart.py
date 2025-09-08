def get_type_multiplier(attacking_type: str, defending_types: list[str]) -> float:
    """
    Type effectiveness chart with a default multiplier for unknown pairs.
    """
    # A simplified chart for demonstration.
    TYPE_EFFECTIVENESS = {
        ("fire", "grass"): 2,
        ("water", "fire"): 2,
        ("fire", "water"): 0.5,
        ("electric", "water"): 2,
        ("normal", "ghost"): 0,
        # Many more type combinations would be added here
    }

    multiplier = 1.0
    for t in defending_types:
        # Get the multiplier from the chart, or default to 1 if not found.
        multiplier *= TYPE_EFFECTIVENESS.get((attacking_type.lower(), t.lower()), 1)
    return multiplier
