import random


def get_live_status():

    grid_health = random.randint(85, 100)

    active_faults = random.randint(0, 5)

    power_supply = random.randint(90, 100)

    disaster = random.choice(
        [
            "LOW",
            "MEDIUM",
            "HIGH"
        ]
    )

    return {
        "Grid Health": grid_health,
        "Faults": active_faults,
        "Power": power_supply,
        "Risk": disaster
    }